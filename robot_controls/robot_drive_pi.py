import serial
import struct
import time
import math
import numpy as np
from pyPS4Controller.controller import Controller


# These are the vendor and product IDs for a PS4 controller.
VENDOR_ID = 0x054C
PRODUCT_ID = 0x05C4


def onStart():
    global connection

    port = '/dev/ttyUSB0' # Device name
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
    global connection

    def onConnect():
        print("Connected to PS4 Controller.")

    def onL3_y(value):
        nonlocal connection
        nonlocal last_vl, last_vr

        left_joystick_y = value
        r2_trigger = controller.get_value('r2')
        l2_trigger = controller.get_value('l2')

        vl, vr = calculate_wheel_velocities(left_joystick_y, r2_trigger, l2_trigger)

        if vl != last_vl or vr != last_vr:
            cmd = struct.pack(">Bhh", 145, vl, vr) # Drirect Drive 5 bytes little endian 
            sendCommandRaw(cmd)
            last_vl, last_vr = vl, vr

    controller = Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listener(onConnect=onConnect, onL3_y=onL3_y)

    last_vl, last_vr = 0, 0


def main():
    onStart()
    time.sleep(1)
    Drive()


if __name__ == "__main__":
    main()
