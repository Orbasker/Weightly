from ultralytics import YOLO


def main():
    # Create a new YOLO model
    model = YOLO('yolov8n.yaml')

    # Train the model
    model.train(
        data='yolov8_dataset/dataset.yaml',
        epochs=100,
        imgsz=640,
        batch=16,
        name='wood_classifier'
    )

    # Evaluate the model
    results = model.val()
    print(results)

    # Make predictions (example)
    results = model('./img.png')
    print(results)

    # Save the model
    model.export()


if __name__ == '__main__':
    main()
