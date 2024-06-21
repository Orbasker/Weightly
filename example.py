import cv2
import numpy as np
from ultralytics import YOLO

# Load the trained model
model = YOLO("path/to/your/trained/model.pt")

# Load an image
image_path = "path/to/your/image.jpg"
image = cv2.imread(image_path)

# Perform inference
results = model(image)

# Process the results
for result in results:
    for box in result.boxes:
        # Extract the bounding box coordinates
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        class_id = box.cls.cpu().numpy().astype(int)[0]
        confidence = box.conf.cpu().numpy()[0]

        # Draw the bounding box on the image
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(
            image,
            f"Class: {class_id}, Conf: {confidence:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2,
        )

        # Estimate the weight (for demonstration purposes, using a fixed conversion factor)
        # In a real scenario, you would use a model to estimate the weight based on object dimensions and type
        item_area = (x2 - x1) * (y2 - y1)
        weight_estimate = item_area * 0.01  # Example conversion factor
        print(f"Estimated weight: {weight_estimate:.2f} grams")

# Show the image with bounding boxes
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
