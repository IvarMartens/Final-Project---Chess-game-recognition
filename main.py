from ultralytics import YOLO
import cv2
import numpy as np
import transform

import ipAddresses

# Load the trained model
model = YOLO('runs/detect/yolov8n_corners/weights/best.pt') 

# Open the pre-shot video file
video_path = 'VID20240507101110.mp4'  # Update with live feed
cap = cv2.VideoCapture(video_path)

# video_feed_url = ipAddresses.home
# cap = cv2.VideoCapture(video_feed_url)

frame_counter = 0
frames_to_skip = 5

def is_square(points):
    # Check if the points form a square
    if len(points) != 4:
        return False

    # Calculate the distance between the points
    d1 = np.sqrt((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2)
    d2 = np.sqrt((points[1][0] - points[2][0])**2 + (points[1][1] - points[2][1])**2)
    d3 = np.sqrt((points[2][0] - points[3][0])**2 + (points[2][1] - points[3][1])**2)
    d4 = np.sqrt((points[3][0] - points[0][0])**2 + (points[3][1] - points[0][1])**2)

    distances = [d1, d2, d3, d4]
    max_distance = max(distances)
    
    for distance in distances:
        if distance < max_distance/3:
            return False
    
    return True


while cap.isOpened():
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        print("Failed to grab frame")
        break

    resized_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)


    # Process only every nth frame
    if frame_counter % frames_to_skip == 0:
        # Make predictions on the current frame
        points = []

        predictions = model.predict(resized_frame)
        boxes = predictions[0].boxes.xyxy.tolist()

        for box in boxes:
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            points.append(center)
        
        if is_square(points):
            np_points = np.array(points, dtype=np.float32)
            transformed_img = transform.four_point_transform(resized_frame, np_points)
            cv2.imshow('Transformed Image', transformed_img)

    frame_counter += 1
    
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

