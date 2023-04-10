import time
from pyPS4Controller.controller import Controller

class MyPS4Controller(Controller):
    def __init__(self, **kwargs):
        super(MyPS4Controller, self).__init__(**kwargs)
        self.left_velocity = 0
        self.right_velocity = 0

    def update_wheel_velocities(self):
        left_velocity = max(min(self.left_velocity, 500), -500)
        right_velocity = max(min(self.right_velocity, 500), -500)
        print(left_velocity, right_velocity)

    def on_L3_up(self, value):
        pass  # Ignore L3 up/down events

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        self.left_velocity += value / 32767 * 500
        self.right_velocity -= value / 32767 * 500
        self.update_wheel_velocities()

    def on_L3_right(self, value):
        self.left_velocity -= value / 32767 * 500
        self.right_velocity += value / 32767 * 500
        self.update_wheel_velocities()

    def on_R2_press(self, value):
        self.left_velocity += value / 255 * 500
        self.right_velocity += value / 255 * 500
        self.update_wheel_velocities()

    def on_L2_press(self, value):
        self.left_velocity -= value / 255 * 500
        self.right_velocity -= value / 255 * 500
        self.update_wheel_velocities()


controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
