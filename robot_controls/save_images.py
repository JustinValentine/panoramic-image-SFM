import cv2
import numpy as np
import time
import os
import glob


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


def empty_images_folder(folder_path):
    files = glob.glob(f"{folder_path}/*.jpg")
    for file in files:
        os.remove(file)


def capture_and_save_photos_from_all_available_cameras(num_photos=1, interval=0.2, folder_path="images", photo=0):
    empty_images_folder(folder_path)

    available_cameras = get_available_cameras()
    if not available_cameras:
        print("No cameras found.")
        return

    caps = [cv2.VideoCapture(index) for index in available_cameras]

    for i in range(num_photos):
        for camera_index, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                file_name = f'{folder_path}/webcam_{camera_index}_photo_{photo}.png'
                cv2.imwrite(file_name, frame)
                print(f"Saved image {i} from camera {camera_index} as {file_name}")
        time.sleep(interval)

    # Release the video capture objects
    for cap in caps:
        cap.release()

if __name__ == "__main__":
    capture_and_save_photos_from_all_available_cameras()