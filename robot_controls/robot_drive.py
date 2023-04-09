import serial, struct, time, math
import numpy as np
import hid
import time


# These are the vendor and product IDs for a PS4 controller.
VENDOR_ID = 0x054C
PRODUCT_ID = 0x05C4


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

            cmd = struct.pack(">Bhh", 145, vl, vr) # Drirect Drive 5 bytes little endian 
            sendCommandRaw(cmd)


            baud_rate = 115200
            sleep_duration = 1 / baud_rate
            
            time.sleep(sleep_duration)

    except KeyboardInterrupt:
        device.close()


def main():
    onStart()
    time.sleep(1)
    Drive()


if __name__ == "__main__":
    main()