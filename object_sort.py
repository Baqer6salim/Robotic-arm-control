#!/usr/bin/env python3
import cv2
import numpy as np
import serial
import time
import sys
from ultralytics import YOLO

# Model path
model_path = "/home/raspbeery4/yolo/my_model_ncnn_model"

# Define sorting positions
positions = {
    "Yellow_Cube": "yellow_obj",
    "Yellow_Rectangle": "yellow_rectangle",
    "Red_Triangle": "red_obj",
    "Red_Rectangle": "red_obj",
    "Red_cylinder": "red_cylinder",
    "Green_Cube": "green_obj",
    "Green_Rectangle": "green_obj",
    "Green_Triangle": "green_obj",
    "Blue_Square": "blue_square",
}

# Initialize serial connection
try:
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"❌ Failed to connect to Arduino: {e}")
    sys.exit(1)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Failed to open the USB webcam.")
    sys.exit(1)

# Load YOLO model
model = YOLO(model_path)

# Bounding box colors
bbox_colors = [
    (164,120,87), (68,148,228), (93,97,209), (178,182,133), (88,159,106),
    (96,202,231), (159,124,168), (169,162,241), (98,118,150), (172,176,184)
]

# Class names
labels = model.names

def send_to_arduino(command):
    """Send command to Arduino and wait for acknowledgment"""
    try:
        arduino.write(f"{command}\n".encode())
        while True:
            if arduino.in_waiting > 0:
                response = arduino.readline().decode().strip()
                if response == "ACK":
                    print(f"✅ Arduino executed: {command}")
                    return True
                elif response == "ERROR":
                    print(f"❌ Arduino failed: {command}")
                    return False
    except Exception as e:
        print(f"❌ Serial communication error: {e}")
        return False

def main():
    print("🚀 Starting YOLO NCNN object detection and sorting system...")
    print("Press 'q' to quit")

    send_to_arduino("home")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break
        
        # Run inference
        results = model(frame, verbose=False)
        detections = results[0].boxes

        detected_objects = []
        
        # Process each detection
        for i in range(len(detections)):
            xyxy = detections[i].xyxy.cpu().numpy().squeeze()
            xmin, ymin, xmax, ymax = xyxy.astype(int)

            class_idx = int(detections[i].cls.item())
            class_name = labels[class_idx]
            conf = detections[i].conf.item()

            # Only consider high-confidence detections
            if conf > 0.5:
                detected_objects.append(class_name)

                # Draw bounding box
                color = bbox_colors[class_idx % len(bbox_colors)]
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                label = f"{class_name}: {int(conf*100)}%"
                label_size, base_line = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
                label_ymin = max(ymin, label_size[1] + 10)
                cv2.rectangle(frame, (xmin, label_ymin-label_size[1]-10), 
                              (xmin+label_size[0], label_ymin+base_line-10), color, cv2.FILLED)
                cv2.putText(frame, label, (xmin, label_ymin-7), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        # Handle detected objects
        if detected_objects:
            print(f"🔍 Detected objects: {', '.join(detected_objects)}")
            
            for obj in detected_objects:
                if obj in positions:
                    if send_to_arduino("pickup"):
                        time.sleep(2)
                        target_pos = positions[obj]
                        if send_to_arduino(target_pos):
                            print(f"📦 Moved {obj} to {target_pos}")
                            time.sleep(2)
                            send_to_arduino("home")
                            time.sleep(1)
                else:
                    print(f"⚠️ No position defined for: {obj}")
        
        # Show frame
        cv2.imshow("YOLO NCNN Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
    print("🛑 System shut down")

if __name__ == "__main__":
    main()
