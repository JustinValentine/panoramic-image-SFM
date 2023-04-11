import cv2
import numpy as np
import time
import os
import datetime

def check_camera_index(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        cap.release()
        return False
    cap.release()
    return True

def get_available_cameras():
    index = 0
    available_cameras = []
    while True:
        if check_camera_index(index):
            available_cameras.append(index)
        else:
            break
        index += 1
    return available_cameras

def create_timestamped_subfolder(parent_folder):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    new_folder = os.path.join(parent_folder, timestamp)
    os.makedirs(new_folder, exist_ok=True)
    return new_folder

def capture_and_save_photos_from_all_available_cameras(num_photos=5, interval=0.2, parent_folder="images"):
    capture_folder = create_timestamped_subfolder(parent_folder)

    available_cameras = get_available_cameras()
    if not available_cameras:
        print("No cameras found.")
        return

    caps = [cv2.VideoCapture(index) for index in available_cameras]

    for i in range(num_photos):
        for camera_index, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                file_name = f'{capture_folder}/webcam_{camera_index}_photo_{i}.jpg'
                cv2.imwrite(file_name, frame)
                print(f"Saved image {i} from camera {camera_index} as {file_name}")
        time.sleep(interval)

    # Release the video capture objects
    for cap in caps:
        cap.release()

if __name__ == "__main__":
    capture_and_save_photos_from_all_available_cameras(num_photos=1)
