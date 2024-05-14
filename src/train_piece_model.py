from ultralytics import YOLO
import torch
import torchvision

def main():
    # Load the model.
    model = YOLO('../Models/yolov8s.pt')

    # Training.
    results = model.train(
        data='Final Project - Chess game recognition/piece data/data.yaml', # Change to correct link
        imgsz=640,
        epochs=80,
        batch=8,
        name='yolov8s_pieces')
    
if __name__ == '__main__':
    main()