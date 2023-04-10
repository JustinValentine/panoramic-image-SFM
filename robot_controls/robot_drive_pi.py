import serial, struct, time, math
import time
from pyPS4Controller.controller import Controller


LEFT_VELOCITY = 0 
RIGHT_VELOCITY = 0 

class MyPS4Controller(Controller):
    def __init__(self, **kwargs):
        super(MyPS4Controller, self).__init__(**kwargs)
        self.left_velocity = 0
        self.right_velocity = 0
        self.prev_l3_value = 0


    def update_wheel_velocities(self):
        global LEFT_VELOCITY, RIGHT_VELOCITY 
        print('vl', self.left_velocity)
        print('vr', self.right_velocity)
        self.left_velocity = max(min(int(self.left_velocity), 500), -500)
        self.right_velocity = max(min(int(self.right_velocity), 500), -500)

        LEFT_VELOCITY = self.left_velocity 
        RIGHT_VELOCITY = self.right_velocity

        print(LEFT_VELOCITY, RIGHT_VELOCITY)


    def on_L3_up(self, value):
        pass  # Ignore L3 up/down events

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        difference = self.prev_l3_value - value
        self.prev_l3_value = value
        self.left_velocity += (difference / 32767) * 500
        self.right_velocity -= (difference / 32767) * 500
        self.update_wheel_velocities()

    def on_L3_right(self, value):
        difference = self.prev_l3_value + value
        self.prev_l3_value = value
        self.left_velocity -= (difference / 32767) * 500
        self.right_velocity += (difference / 32767) * 500
        self.update_wheel_velocities()

    def on_R2_press(self, value):
        # print('on_R2_press', (value / 32767) * 500)
        self.left_velocity = abs((value / 32767) * 500)
        self.right_velocity = abs((value / 32767) * 500)
        self.update_wheel_velocities()

    def on_L2_press(self, value):
        # print('on_L2_press', (value / 32767) * 500)
        self.left_velocity = -1*abs((value / 32767) * 500)
        self.right_velocity = -1*abs((value / 32767) * 500)
        self.update_wheel_velocities()


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


def Drive():

    controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()

    while True:
        cmd = struct.pack(">Bhh", 145, LEFT_VELOCITY, RIGHT_VELOCITY) # Drirect Drive 5 bytes little endian 
        sendCommandRaw(cmd)


        baud_rate = 115200
        sleep_duration = 1 / baud_rate
        
        time.sleep(sleep_duration)


def main():
    onStart()
    time.sleep(1)
    Drive()


if __name__ == "__main__":
    main()
