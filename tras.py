import os
import shutil
import random

# Define dataset paths
image_source_folder = "C:/Users/DELL/Yolo/muslim_images/"
label_source_folder = "C:/Users/DELL/Yolo/muslim_txtlabels/"

base_path = "C:/Users/DELL/Yolo/dataset"
image_train_path = os.path.join(base_path, "images", "train")
image_val_path = os.path.join(base_path, "images", "val")
label_train_path = os.path.join(base_path, "labels", "train")
label_val_path = os.path.join(base_path, "labels", "val")

# Ensure directories exist
os.makedirs(image_train_path, exist_ok=True)
os.makedirs(image_val_path, exist_ok=True)
os.makedirs(label_train_path, exist_ok=True)
os.makedirs(label_val_path, exist_ok=True)

# Get all image files
image_files = [f for f in os.listdir(image_source_folder) if f.endswith((".jpg", ".png"))]

# Shuffle and split dataset
random.shuffle(image_files)
split_index = int(0.8 * len(image_files))
train_files = image_files[:split_index]
val_files = image_files[split_index:]

# Function to move images and labels
def move_files(image_list, image_dest, label_dest):
    for image_file in image_list:
        label_file = os.path.splitext(image_file)[0] + ".txt"
        image_src_path = os.path.join(image_source_folder, image_file)
        label_src_path = os.path.join(label_source_folder, label_file)
        image_dest_path = os.path.join(image_dest, image_file)
        label_dest_path = os.path.join(label_dest, label_file)

        if os.path.exists(image_src_path):
            shutil.copy(image_src_path, image_dest_path)
        if os.path.exists(label_src_path):
            shutil.copy(label_src_path, label_dest_path)

# Move files to folders
move_files(train_files, image_train_path, label_train_path)
move_files(val_files, image_val_path, label_val_path)

print(f"✅ Done! {len(train_files)} training images, {len(val_files)} validation images.")
