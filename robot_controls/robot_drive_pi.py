import serial
import struct
import time
from pyPS4Controller.controller import Controller
# from save_images import capture_and_save_photos_from_all_available_cameras

class MyPS4Controller(Controller):
    def __init__(self, interface, connecting_using_ds4drv, velocity_callback):
        super(MyPS4Controller, self).__init__(interface=interface, connecting_using_ds4drv=connecting_using_ds4drv)

        self.max_velocity = 75

        self.left_velocity = 0
        self.right_velocity = 0

        self.r2_trigger = 0
        self.l2_trigger = 0
        self.left_joystick_y = 0
        
        self.velocity_callback = velocity_callback
        self.connection = None

        self.start_serial()
        time.sleep(1)

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


    def calculate_wheel_velocities(self):
        linear_vel = self.max_velocity * self.r2_trigger + self.l2_trigger * self.max_velocity

        if self.left_joystick_y < 0:
            self.left_velocity = int(linear_vel - (self.left_joystick_y * self.max_velocity))
            self.right_velocity = int(linear_vel)

        else:
            self.left_velocity = int(linear_vel)
            self.right_velocity = int(linear_vel + (self.left_joystick_y * self.max_velocity))

        print(self.left_velocity , self.right_velocity, self.left_joystick_y)


    def update_wheel_velocities(self):
        self.calculate_wheel_velocities()

        self.velocity_callback(self.left_velocity, self.right_velocity)
        
        cmd = struct.pack(">Bhh", 145, self.left_velocity, self.right_velocity)
        self.send_command_raw(cmd)


    def on_x_press(self):
        # Turn with wheel speeds of -25 and 25
        cmd = struct.pack(">Bhh", 145, -25, 25)
        self.send_command_raw(cmd)

        # Capture and save photos from all available cameras
        print("Capturing and saving photos from all available cameras")
        # capture_and_save_photos_from_all_available_cameras()


    def on_x_release(self):
        # Stop the robot
        cmd = struct.pack(">Bhh", 145, 0, 0)
        self.send_command_raw(cmd)


    def on_circle_press(self):
        cmd = struct.pack(">Bhh", 145, -30, 30)
        self.send_command_raw(cmd)


    def on_circle_release(self):
        cmd = struct.pack(">Bhh", 145, 0, 0)
        self.send_command_raw(cmd)


    def on_square_press(self):
        cmd = struct.pack(">Bhh", 145, 30, -30)
        self.send_command_raw(cmd)


    def on_square_release(self):
        cmd = struct.pack(">Bhh", 145, 0, 0)
        self.send_command_raw(cmd)


    def on_L3_up(self, value):
        pass


    def on_L3_down(self, value):
        pass


    def on_L3_left(self, value):
        self.left_joystick_y = value / 32767
        self.update_wheel_velocities()


    def on_L3_right(self, value):
        self.left_joystick_y = value / 32767
        self.update_wheel_velocities()


    def on_L3_x_at_rest(self):
        self.left_joystick_y  = 0
        self.update_wheel_velocities()


    def on_R2_press(self, value):
        self.r2_trigger = value / 32767
        self.update_wheel_velocities()


    def on_L2_press(self, value):
        self.l2_trigger = -1 * value / 32767
        self.update_wheel_velocities()


    def on_R2_release(self):
        self.r2_trigger = 0
        self.update_wheel_velocities()


    def on_L2_release(self):
        self.l2_trigger= 0
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
    controller.listen()

if __name__ == "__main__":
    main()