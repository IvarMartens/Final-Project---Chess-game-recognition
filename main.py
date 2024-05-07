from ultralytics import YOLO
import cv2
import numpy as np
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
frames_to_skip = 5


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
        
        if helper.is_square(points):
            np_points = np.array(points, dtype=np.float32)
            transformed_img = transform.four_point_transform(resized_frame, np_points)
            cv2.imshow('Transformed Image', transformed_img)

    frame_counter += 1
    
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

