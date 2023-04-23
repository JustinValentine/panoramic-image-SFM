import serial, struct, time, math
import numpy as np
import hid
import time

import cv2
import os
import glob

# These are the vendor and product IDs for a PS4 controller.
VENDOR_ID = 0x054C
PRODUCT_ID = 0x05C4


baud_rate = 115200
sleep_duration = 1 / baud_rate


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


def onStart():
    global connection

    port = '/dev/tty.usbserial-DN0267KP' # Device name
    Baudrate = 115200 # rate at which information is transferred in a communication channel
    Timeout = 1 # Set a read timeout value in seconds

    try:
        connection = serial.Serial(port, baudrate=Baudrate, timeout=Timeout)
        sendCommandASCII('128') # Send start command
        sendCommandASCII('131') # Send command to Enter FULL mode 
        print("Connected!")

    except:
        print("Failed.")


def sendCommandASCII(command):
    cmd = bytes([int(v) for v in command.split()]) # An empty bytes object of the specified sizes will be created
    sendCommandRaw(cmd)


def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            assert isinstance(command, bytes) # Check if commad is of type bytes 
            connection.write(command) # Write the bytes data to the port
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


def Drive(available_cameras):

    device = connect_ps4_controller()
    if device is None:
        return

    try:
        while True:
            data = device.read(64)

            if len(data) > 0:
                left_joystick_y = data[1]
                print(data)
                r2_trigger = data[-1]
                l2_trigger = data[-2]
                x_trigger = data[5]

                vl, vr = calculate_wheel_velocities(left_joystick_y, r2_trigger, l2_trigger)

            else:
                vl, vr = 0, 0

            if x_trigger == 40:

                for i in range(3):
                    start_time = time.time()
                    while time.time() - start_time < 0.1:
                        cmd = struct.pack(">Bhh", 145, 25, -25) # Drirect Drive 5 bytes little endian 
                        sendCommandRaw(cmd)
                        time.sleep(sleep_duration)

                    cmd = struct.pack(">Bhh", 145, 0, 0) # Drirect Drive 5 bytes little endian 
                    sendCommandRaw(cmd)

                    print("Capturing and saving photos from all available cameras")
                    capture_image(available_cameras, photo=i)
                    time.sleep(0.1)
                break
            
            else:
                cmd = struct.pack(">Bhh", 145, vl, vr) # Drirect Drive 5 bytes little endian 
                sendCommandRaw(cmd)
                
                time.sleep(sleep_duration)

    except KeyboardInterrupt:
        device.close()


def capture_image(available_cameras, folder_path="images", photo=0):
    caps = [cv2.VideoCapture(index) for index in available_cameras]

    for camera_index, cap in enumerate(caps):
        ret, frame = cap.read()
        if ret:
            file_name = f'{folder_path}/webcam_{camera_index}_photo_{photo}.png'
            cv2.imwrite(file_name, frame)
            print(f"Saved image {photo} from camera {camera_index} as {file_name}")


def main():
    onStart()

    empty_images_folder(folder_path="images")

    available_cameras = get_available_cameras()

    if not available_cameras:
        print("No cameras found.")
        return

    time.sleep(1)

    Drive(available_cameras)


if __name__ == "__main__":
    main()