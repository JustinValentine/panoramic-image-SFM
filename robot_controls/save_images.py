import cv2
import os
import time

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

def capture_and_save_photos_from_all_available_cameras():
    available_cameras = get_available_cameras()
    if not available_cameras:
        print("No cameras found.")
        return

    caps = [cv2.VideoCapture(index) for index in available_cameras]

    for camera_index, cap in enumerate(caps):
        ret, frame = cap.read()
        if ret:
            current_time = int(time.time())
            folder_name = str(camera_index)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_name = f'{folder_name}/{current_time}.jpg'
            cv2.imwrite(file_name, frame)
            print(f"Saved image from camera {camera_index} as {file_name}")

    # Release the video capture objects
    for cap in caps:
        cap.release()

if __name__ == "__main__":
    capture_and_save_photos_from_all_available_cameras()
