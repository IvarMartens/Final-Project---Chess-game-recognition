from ultralytics import YOLO

def main():
    # Load the model.
    model = YOLO('yolov8n.pt')

    # Training.
    results = model.train(
        data='Final Project - Chess game recognition/corner data/data.yaml', # change to correct link 
        imgsz=640,
        epochs=100,
        batch=8,
        name='yolov8n_corners')

if __name__ == '__main__':
    main()