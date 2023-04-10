import serial
import struct
import time
from pyPS4Controller.controller import Controller

class MyPS4Controller(Controller):
    def __init__(self, interface, connecting_using_ds4drv, velocity_callback):
        super(MyPS4Controller, self).__init__(interface=interface, connecting_using_ds4drv=connecting_using_ds4drv)
        self.left_velocity = 0
        self.right_velocity = 0
        self.prev_l3_value = 0
        self.velocity_callback = velocity_callback
        self.connection = None

        self.start_serial()
        time.sleep(1)
        self.listen()

    def start_serial(self):
        port = '/dev/ttyUSB0'
        baud_rate = 115200
        timeout = 1

        try:
            self.connection = serial.Serial(port, baudrate=baud_rate, timeout=timeout)
            self.send_command_ascii('128')
            self.send_command_ascii('131')
            print("Connected!")
        except:
            print("Failed.")

    def send_command_ascii(self, command):
        cmd = bytes([int(v) for v in command.split()])
        self.send_command_raw(cmd)

    def send_command_raw(self, command):
        try:
            if self.connection is not None:
                assert isinstance(command, bytes)
                self.connection.write(command)
                self.connection.flush()
            else:
                print("Not connected.")
        except serial.SerialException:
            print("Lost connection")
            self.connection = None

    def update_wheel_velocities(self):
        self.left_velocity = max(min(int(self.left_velocity), 500), -500)
        self.right_velocity = max(min(int(self.right_velocity), 500), -500)
        self.velocity_callback(self.left_velocity, self.right_velocity)

    def on_L3_up(self, value):
        pass

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
        self.left_velocity = abs((value / 32767) * 500)
        self.right_velocity = abs((value / 32767) * 500)
        self.update_wheel_velocities()

    def on_L2_press(self, value):
        self.left_velocity = -1 * abs((value / 32767) * 500)
        self.right_velocity = -1 * abs((value / 32767) * 500)
        self.update_wheel_velocities()

    def drive(self):
        while True:
            print('robot', self.left_velocity, self.right_velocity)
            cmd = struct.pack(">Bhh", 145, self.left_velocity, self.right_velocity)
            self.send_command_raw(cmd)

            sleep_duration = 1 / 115200
            time.sleep(sleep_duration)


def velocity_callback(left_velocity, right_velocity):
    print('Robot:', left_velocity, right_velocity)


def main():
    controller = MyPS4Controller(
        interface="/dev/input/js0",
        connecting_using_ds4drv=False,
        velocity_callback=velocity_callback,
    )
    controller.drive()
