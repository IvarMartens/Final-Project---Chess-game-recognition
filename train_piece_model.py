from ultralytics import YOLO
import torch
import torchvision

def main():
    # Load the model.
    model = YOLO('yolov8s.pt')
    torch.cuda.empty_cache()
    print(torch.cuda.memory_summary(device=None, abbreviated=False))

    # Training.
    results = model.train(
        data='C:/Users/ivar/Documents/Documents/University/Leiden University/Master/Robotics/Final Project - Chess game recognition/piece data/data.yaml',
        imgsz=640,
        epochs=80,
        batch=16,
        name='yolov8s_pieces')
    
if __name__ == '__main__':
    main()