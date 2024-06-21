from ultralytics import YOLO

# Load a YOLOv8 model (pre-trained on COCO dataset)
model = YOLO("yolov8n.pt")

# Train the model on your dataset
model.train(data="datasets/pets/dataset.yaml", epochs=1, imgsz=640)
