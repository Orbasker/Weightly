import os
import shutil
from sklearn.model_selection import train_test_split

def prepare_yolov8_dataset(input_dir, output_dir, class_mapping_file, train_ratio=0.8):
    # Create necessary directories
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)

    # Read class mapping
    class_mapping = {}
    with open(class_mapping_file, 'r') as f:
        for line in f:
            class_id, class_name = line.strip().split(' ', 1)
            class_mapping[class_name] = int(class_id)

    # Get all image files
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

    # Split into train and validation sets
    train_files, val_files = train_test_split(image_files, train_size=train_ratio)

    # Function to create a label file
    def create_label_file(image_file, label_dir):
        class_name = os.path.splitext(image_file)[0].replace('_', ' ')
        class_id = class_mapping[class_name]
        label_file = os.path.join(label_dir, os.path.splitext(image_file)[0] + '.txt')
        with open(label_file, 'w') as f:
            # Format: <class> <x_center> <y_center> <width> <height>
            # Assuming the wood occupies the entire image
            f.write(f'{class_id} 0.5 0.5 1.0 1.0\n')

    # Process train files
    for image_file in train_files:
        shutil.copy(os.path.join(input_dir, image_file), 
                    os.path.join(output_dir, 'images', 'train', image_file))
        create_label_file(image_file, os.path.join(output_dir, 'labels', 'train'))

    # Process validation files
    for image_file in val_files:
        shutil.copy(os.path.join(input_dir, image_file), 
                    os.path.join(output_dir, 'images', 'val', image_file))
        create_label_file(image_file, os.path.join(output_dir, 'labels', 'val'))

    print(f"Dataset prepared: {len(train_files)} training images, {len(val_files)} validation images")

    # Create dataset.yaml file
    with open(os.path.join(output_dir, 'dataset.yaml'), 'w') as f:
        f.write(f"path: {os.path.abspath(output_dir)}\n")
        f.write("train: images/train\n")
        f.write("val: images/val\n")
        f.write(f"nc: {len(class_mapping)}\n")
        f.write(f"names: {list(class_mapping.keys())}\n")

# Usage
input_dir = 'wood_images'
output_dir = 'yolov8_dataset'
class_mapping_file = 'class_mapping.txt'
prepare_yolov8_dataset(input_dir, output_dir, class_mapping_file)
