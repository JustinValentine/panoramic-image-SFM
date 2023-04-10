import serial, struct, time, math
import numpy as np
from pyPS4Controller.controller import Controller
import time

# These are the vendor and product IDs for a PS4 controller.
VENDOR_ID = 0x054C
PRODUCT_ID = 0x05C4

def onStart():
    global connection

    port = '/dev/tty.usbserial-DN0267KP'  # Device name
    Baudrate = 115200  # rate at which information is transferred in a communication channel
    Timeout = 1  # Set a read timeout value in seconds

    try:
        connection = serial.Serial(port, baudrate=Baudrate, timeout=Timeout)
        sendCommandASCII('128')  # Send start command
        sendCommandASCII('131')  # Send command to Enter FULL mode
        print("Connected!")

    except:
        print("Failed.")

def sendCommandASCII(command):
    cmd = bytes([int(v) for v in command.split()])  # An empty bytes object of the specified sizes will be created
    sendCommandRaw(cmd)

def sendCommandRaw(command):
    global connection

    try:
        if connection is not None:
            assert isinstance(command, bytes)  # Check if commad is of type bytes
            connection.write(command)  # Write the bytes data to the port
            connection.flush()
        else:
            print("Not connected.")

    except serial.SerialException:
        print("Lost connection")
        connection = None

class MyPS4Controller(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.left_joystick_y = 0
        self.r2_trigger = 0
        self.l2_trigger = 0

    def on_left_analog(self, x, y):
        self.left_joystick_y = y

    def on_R2_press(self, value):
        self.r2_trigger = value

    def on_L2_press(self, value):
        self.l2_trigger = value

    def send_wheel_commands(self):
        vl, vr = calculate_wheel_velocities(self.left_joystick_y, self.r2_trigger, self.l2_trigger)

        cmd = struct.pack(">Bhh", 145, vl, vr)  # Direct Drive 5 bytes little endian
        sendCommandRaw(cmd)

        baud_rate = 115200
        sleep_duration = 1 / baud_rate
        time.sleep(sleep_duration)

def calculate_wheel_velocities(left_joystick_y, r2_trigger, l2_trigger, v_max=200):

    left_joystick_y = (left_joystick_y - 127) / 127
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

    controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=0.01)

    try:
        while True:
            controller.send_wheel_commands()

    except KeyboardInterrupt:
        controller.stop()


def main():
    onStart()
    time.sleep(1)
    Drive()


if __name__ == "__main__":
    main()