from ultralytics import YOLO
import cv2
import numpy as np
import torch
import torchvision
import sys

import transform
import helper
import visualise_board

# Load the trained model
model_corners = YOLO('runs/detect/yolov8n_corners/weights/best.pt')
model_pieces = YOLO('runs/detect/yolov8s_pieces/weights/best.pt')

# Open the pre-shot video file
video_path = 'test_videos/VIDM4.mp4'  
cap = cv2.VideoCapture(video_path)

#video_feed_url = helper.get_ip('uni')
#cap = cv2.VideoCapture(video_feed_url)

frame_counter = 0
frames_to_skip = 10

circle_radius = 5
circle_color_red = (0, 0, 255)  # Red color
circle_color_blue = (255, 0, 0)
thickness = -1  # Filled circle

old_fen = ''
turn = 'w'
last_move = None

#out = cv2.VideoWriter("test_videos\VIDM4.mp4", -1, 20.0, (640,480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    #out.write(frame)

    resized_frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)

    # Process only every nth frame
    if frame_counter % frames_to_skip == 0:

        #predict corners
        predictions = model_corners.predict(resized_frame, show=False, verbose=False)

        # Get location of the corners
        boxes = predictions[0].boxes.xyxy.tolist()
        points = []
        for box in boxes:
            center = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
            points.append(center)
        
        #check if points form a square, and which points form that square (sometimes the model detects more than 4 points)
        is_square, good_points = helper.is_square(points)
        if is_square:
            np_points = np.array(good_points, dtype=np.float32)

            #Transform the image to a topdown view
            topdown_img, M = transform.four_point_transform(resized_frame, np_points)
            height, width = topdown_img.shape[:2]

            # turn chessboard if were not looking from white side (Bottom left corner is not darker than the bottom right corner)
            transformed_img, turned = helper.adjust_chessboard_orientation(topdown_img, height, width)
            height_transformed, width_transformed = transformed_img.shape[:2]

    
            section_height = transformed_img.shape[0] // 8
            section_width = transformed_img.shape[1] // 8

            grid_points = [[],[]]
            
            # Loop through rows and columns to find coordinates of the intersection points
            for row in range(1,8):
                for col in range(1,8):
                    x = col * section_width
                    y = row * section_height

                    if x not in grid_points[0]:
                        grid_points[0].append(x)
                grid_points[1].append(y)

            # Draw the grid on the transformed image
            for x in grid_points[0]:
                cv2.line(transformed_img, (x, 0), (x, height_transformed), (255, 0, 0), 2)
            for y in grid_points[1]:
                cv2.line(transformed_img, (0, y), (width_transformed, y), (0, 255, 0), 2)

            # Predict the pieces on normal image
            pieces_predictions = model_pieces.predict(resized_frame, show=False, verbose=False)

            pieces_boxes = pieces_predictions[0].boxes.xyxy.tolist()
            pieces_classes = pieces_predictions[0].boxes.cls.tolist()
            pieces_names = pieces_predictions[0].names
            pieces_confidences = pieces_predictions[0].boxes.conf.tolist()

            # Fit the predictions to the transformed image
            transformed_boxes_points = helper.transform_boxes(pieces_boxes, M)
            correct_points = helper.rotate_points(transformed_boxes_points, turned, height, width)

            for point in correct_points:
                cv2.circle(transformed_img, (int(point[0]), int(point[1])), circle_radius, circle_color_red, thickness)

            cv2.imshow('Transformed Image', transformed_img)

            # get positioning within grid
            locations = []
            names = []
            for i in range(len(correct_points)):
                box_point = correct_points[i]
                location = helper.is_in_location(box_point, grid_points, height_transformed, width_transformed)      
                if location not in locations:
                    locations.append(location)
                    names.append(pieces_names[pieces_classes[i]])
                else:
                    #find index of the location in the list
                    index = locations.index(location)
                    if pieces_confidences[i] > pieces_confidences[index]:
                        locations[index] = location
                        name = pieces_names[pieces_classes[i]]
                        names[index] = name
                    else:
                        continue
            
            # remove None values
            none_location_index = [i for i, x in enumerate(locations) if x == None]
            for i in none_location_index:
                locations.pop(i)
                names.pop(i)

            # Convert locations to FEN
            fen = helper.create_fen(locations, names, turn)

            if old_fen != '':
                board = visualise_board.visualise_board(fen, None)
                cv2.imshow('Detected Board', board)

            legal, move = helper.is_legal_move(old_fen, fen)
            # check if move is legal
            if legal:
                last_move = move
                old_fen = fen
                if turn == 'w':
                    turn = 'b'
                else:
                    turn = 'w'

            if old_fen != '':
                board = visualise_board.visualise_board(old_fen, last_move)
                cv2.imshow('Board', board)

            #cv2.waitKey(0)
            
    frame_counter += 1
    
    
    # Break the loop with the 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()