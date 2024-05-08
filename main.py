from ultralytics import YOLO
import cv2
import numpy as np
import torch
import torchvision
import sys

import transform
import helper


# Load the trained model
model = YOLO('runs/detect/yolov8n_corners/weights/best.pt') 

# Open the pre-shot video file
video_path = 'VID20240507101110.mp4'  # Update with live feed
cap = cv2.VideoCapture(video_path)

# video_feed_url = helper.get_ip('home')
# cap = cv2.VideoCapture(video_feed_url)

frame_counter = 0
frames_to_skip = 2

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

        predictions = model.predict(resized_frame, show=True, device='cuda:0')
        boxes = predictions[0].boxes.xyxy.tolist()

        for box in boxes:
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            points.append(center)
        
        is_square, good_points = helper.is_square(points)
        if is_square:
            np_points = np.array(good_points, dtype=np.float32)
            topdown_img = transform.four_point_transform(resized_frame, np_points)
            height, width = topdown_img.shape[:2]
   
            transformed_img = helper.adjust_chessboard_orientation(topdown_img, height, width)

            section_height = transformed_img.shape[0] // 8
            section_width = transformed_img.shape[1] // 8

            grid_points = [[],[]]
            
            # Loop through rows and columns to find coordinates of the intersection points
            for row in range(1,8):
                for col in range(1,8):
                    x = col * section_width
                    y = row * section_height

                    if y not in grid_points[1]:
                        grid_points[1].append(y)
                    
                    # Draw circles on each intersection point
                    circle_radius = 5
                    circle_color = (0, 0, 255)  # Red color
                    thickness = -1  # Filled circle

                    cv2.circle(transformed_img, (x, y), circle_radius, circle_color, thickness)
                
                grid_points[0].append(x)

            cv2.imshow('Transformed Image', transformed_img)
            cv2.waitKey(0)

    frame_counter += 1
    print(f"Frame: {frame_counter}")
    
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

