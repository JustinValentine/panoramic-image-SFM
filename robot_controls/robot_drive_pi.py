import serial
import struct
import time
from pyPS4Controller.controller import Controller

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

    def get_encoder_counts(self):
        # Send the "Query List" command (149) with the encoder count packet IDs
        # Packet ID 43 for left wheel encoder count
        # Packet ID 44 for right wheel encoder count
        cmd = struct.pack(">BBBB", 149, 2, 43, 44)
        self.send_command_raw(cmd)

        # Read the response (2 bytes for each encoder count, plus 1 byte for the packet ID)
        response = self.connection.read(5)

        if len(response) == 5:
            left_encoder_count = struct.unpack(">h", response[1:3])[0]
            right_encoder_count = struct.unpack(">h", response[3:5])[0]
            print(left_encoder_count, right_encoder_count) 
        else:
            print("Warning: Received an incomplete response from the robot.")


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
        # self.get_encoder_counts()

        self.velocity_callback(self.left_velocity, self.right_velocity)
        
        cmd = struct.pack(">Bhh", 145, self.left_velocity, self.right_velocity)
        self.send_command_raw(cmd)

    def on_circle_press(self):
        cmd = struct.pack(">Bhh", 145, 50, -50)
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

