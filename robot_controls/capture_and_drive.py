import cv2
import numpy as np
import os
import time
import serial
import struct
import math
import hid
import threading

VENDOR_ID = 0x054C
PRODUCT_ID = 0x05C4


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


def onStart():
    global connection

    port = '/dev/tty.usbserial-DN0267KP'
    Baudrate = 115200
    Timeout = 1

    try:
        connection = serial.Serial(port, baudrate=Baudrate, timeout=Timeout)
        sendCommandASCII('128')
        sendCommandASCII('131')
        print("Connected!")

    except:
        print("Failed.")


def sendCommandASCII(command):
    cmd = bytes([int(v) for v in command.split()])
    sendCommandRaw(cmd)


def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            assert isinstance(command, bytes)
            connection.write(command)
            connection.flush()
        else:
            print("Not connected.")

    except serial.SerialException:
        print("Lost connection")
        connection = None


def connect_ps4_controller():
    devices = hid.enumerate(VENDOR_ID, PRODUCT_ID)
    if len(devices) == 0:
        print("No PS4 controller found.")
        return None

    device_info = devices[0]
    device = hid.device()
    device.open_path(device_info['path'])
    return device


def calculate_wheel_velocities(left_joystick_y, r2_trigger, l2_trigger, v_max=200):

    left_joystick_y = (left_joystick_y - 127)/127
    r2_trigger /= 255
    l2_trigger /= -255

    linear_vel = v_max * r2_trigger + l2_trigger * v_max

    if left_joystick_y < 0:
        vl = linear_vel - (left_joystick_y * v_max)
        vr = linear_vel

    else:
        vl = linear_vel
        vr = linear_vel + (left_joystick_y * v_max)

    print(int(vl), int(vr), left_joystick_y)

    return int(vl), int(vr)


def Drive():
    device = connect_ps4_controller()
    if device is None:
        return

    try:
        while True:
            data = device.read(64)

            if len(data) > 0:
                left_joystick_y = data[1]
                r2_trigger = data[-1]
                l2_trigger = data[-2]

                vl, vr = calculate_wheel_velocities(left_joystick_y, r2_trigger, l2_trigger)

            else:
                vl, vr = 0, 0

            cmd = struct.pack(">Bhh", 145, vl, vr)
            sendCommandRaw(cmd)

            baud_rate = 115200
            sleep_duration = 1 / baud_rate

            time.sleep(sleep_duration)

    except KeyboardInterrupt:
        device.close()


def capture_and_drive():
    camera_thread = threading.Thread(target=capture_and_save_photos_from_all_available_cameras)
    drive_thread = threading.Thread(target=Drive)

    camera_thread.start()
    drive_thread.start()

    camera_thread.join()
    drive_thread.join()


def main():
    onStart()
    time.sleep(1)
    capture_and_drive()


if __name__ == "__main__":
    main()