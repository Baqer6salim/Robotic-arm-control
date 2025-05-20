import cv2
import os
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# Folder to save images
save_folder = "C:/Users/DELL/Yolo/muslim_images"

# Ensure the folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Function to get next available filename
def get_next_filename():
    existing_files = sorted([f for f in os.listdir(save_folder) if f.startswith("image_ext") and f.endswith(".jpg")])
    if existing_files:
        last_file = existing_files[-1]
        last_number = int(last_file[9:12])  # Extract number from 'imageXXX.jpg'
        next_number = last_number + 1
    else:
        next_number = 1
    return f"image_ext{next_number:03d}.jpg"  # Format as image001, image002, etc.

# Function to capture and save image
def capture_image():
    if frame is not None:
        filename = get_next_filename()
        filepath = os.path.join(save_folder, filename)
        cv2.imwrite(filepath, frame)
        status_label.config(text=f"Image saved as {filename}", fg="green")

# Function to update the video feed in the GUI
def update_preview():
    global frame
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.config(image=imgtk)
    camera_label.after(10, update_preview)  # Refresh every 10ms

# Create GUI
root = tk.Tk()
root.title("USB Webcam Image Capture")

# Open webcam (Change 1 if needed)
cap = cv2.VideoCapture(1)  # 0 = Laptop Camera, 1 = External USB Camera

# Live Camera Preview
camera_label = Label(root)
camera_label.pack()

# Capture Button
capture_button = tk.Button(root, text="Capture Image", command=capture_image, font=("Arial", 30))
capture_button.pack(pady=20)

# Status Label
status_label = Label(root, text="", font=("Arial", 20))
status_label.pack()

# Start live preview
update_preview()

# Run GUI loop
root.mainloop()

# Release camera when GUI is closed
cap.release()
cv2.destroyAllWindows()
