import cv2
import numpy as np
import ipAddresses

video_feed_url = ipAddresses.home
cap = cv2.VideoCapture(video_feed_url)

chessboard_size = (7, 7)  # 7x7 internal corners

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Attempt to find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

    # Only display the frame if the chessboard was found
    if ret == True:
        # Enhances the corner detection
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        # Draw and display the corners
        cv2.drawChessboardCorners(frame, chessboard_size, corners2, ret)
        cv2.imshow('Chessboard Detection', frame)
    else:
        # Optional: Display a message or a blank screen if the chessboard is not detected
        # cv2.imshow('Chessboard Detection', np.zeros_like(frame))
        pass

    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()