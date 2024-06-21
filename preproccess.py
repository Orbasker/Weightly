import os
import xml.etree.ElementTree as ET
import glob
import random

# Define paths
image_path = "datasets/pets/images"
annotation_path = "datasets/pets/annotations"
label_path = "datasets/pets/labels"

# Create directories for images and labels
os.makedirs(f"{image_path}/train", exist_ok=True)
os.makedirs(f"{image_path}/val", exist_ok=True)
os.makedirs(f"{label_path}/train", exist_ok=True)
os.makedirs(f"{label_path}/val", exist_ok=True)


def convert(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open(f"{annotation_path}/xmls/{image_id}.xml")
    out_file = open(f"{label_path}/{image_id}.txt", "w")
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    for obj in root.iter("object"):
        cls = obj.find("name").text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find("bndbox")
        b = (
            float(xmlbox.find("xmin").text),
            float(xmlbox.find("xmax").text),
            float(xmlbox.find("ymin").text),
            float(xmlbox.find("ymax").text),
        )
        bb = convert((w, h), b)
        out_file.write(f"{cls_id} " + " ".join([str(a) for a in bb]) + "\n")


# Define class names
classes = ["cat", "dog"]

# Convert annotations
xml_files = glob.glob(f"{annotation_path}/xmls/*.xml")
for xml_file in xml_files:
    image_id = os.path.basename(xml_file).replace(".xml", "")
    convert_annotation(image_id)

# Get list of all images
image_files = glob.glob(f"{image_path}/*.jpg")

# Shuffle and split the dataset
random.shuffle(image_files)
split_index = int(len(image_files) * 0.8)
train_files = image_files[:split_index]
val_files = image_files[split_index:]

# Write train.txt and val.txt
with open(f"{annotation_path}/train.txt", "w") as f:
    for file in train_files:
        f.write(os.path.basename(file).replace(".jpg", "") + "\n")

with open(f"{annotation_path}/val.txt", "w") as f:
    for file in val_files:
        f.write(os.path.basename(file).replace(".jpg", "") + "\n")

# Move the images and labels to their respective directories
for file in train_files:
    os.rename(file, f"{image_path}/train/{os.path.basename(file)}")
    os.rename(
        f'{label_path}/{os.path.basename(file).replace(".jpg", ".txt")}',
        f'{label_path}/train/{os.path.basename(file).replace(".jpg", ".txt")}',
    )

for file in val_files:
    os.rename(file, f"{image_path}/val/{os.path.basename(file)}")
    os.rename(
        f'{label_path}/{os.path.basename(file).replace(".jpg", ".txt")}',
        f'{label_path}/val/{os.path.basename(file).replace(".jpg", ".txt")}',
    )
