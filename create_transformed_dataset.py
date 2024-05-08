from ultralytics import YOLO
import cv2
import numpy as np
import torch
import torchvision
import sys
from os import listdir

import transform
import helper

# Load the trained model
model = YOLO('runs/detect/yolov8n_corners4/weights/best.pt')
folder = "unlabeled piece data/new"
images = "C:/Users/ivar/Documents/Documents/University/Leiden University/Master/Robotics/piece Images/new/"

i = 1
for image in listdir(images):
    image = cv2.imread(images + image)
    resized_frame = cv2.resize(image, (640, 480), interpolation = cv2.INTER_AREA)
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

        cv2.imwrite(f"{folder}/picture{i}.png", transformed_img)
        i += 1
    else:
        print("No square found")
