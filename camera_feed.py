import cv2
import numpy as np
import ipAdresses

video_feed_url = ipAdresses.home
cap = cv2.VideoCapture(video_feed_url)

def is_consistent(gaps, tolerance=0.2):
    avg_gap = np.mean(gaps)
    return all(abs(gap - avg_gap) / avg_gap < tolerance for gap in gaps)

def find_consistent_sequences(lines, is_horizontal=True, tolerance=0.2, length_tolerance=0.2):
    if not lines:
        return []
    
    lengths = [np.sqrt((line[2] - line[0])**2 + (line[3] - line[1])**2) for line in lines]
    median_length = np.median(lengths)
    length_filtered_lines = [line for line, length in zip(lines, lengths) if abs(length - median_length) / median_length < length_tolerance]
    
    sorted_lines = sorted(length_filtered_lines, key=lambda line: (line[0] + line[2]) // 2 if is_horizontal else (line[1] + line[3]) // 2)
    gaps = [sorted_lines[i + 1][1] - sorted_lines[i][3] if is_horizontal else sorted_lines[i + 1][0] - sorted_lines[i][2] for i in range(len(sorted_lines) - 1)]
    
    for i in range(len(gaps) - 7):
        if is_consistent(gaps[i:i + 8], tolerance):
            return sorted_lines[i:i + 9]
    return []

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=10)

    if lines is not None:
        horizontal_lines = [line[0] for line in lines if abs(line[0][1] - line[0][3]) < 20]
        vertical_lines = [line[0] for line in lines if abs(line[0][0] - line[0][2]) < 20]

        consistent_horizontals = find_consistent_sequences(horizontal_lines, is_horizontal=True, length_tolerance=0.2)
        consistent_verticals = find_consistent_sequences(vertical_lines, is_horizontal=False, length_tolerance=0.2)

        for x1, y1, x2, y2 in consistent_horizontals + consistent_verticals:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Detected Lines', frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    process_frame(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()