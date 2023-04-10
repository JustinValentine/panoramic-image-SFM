import time
from pyPS4Controller.controller import Controller

class MyPS4Controller(Controller):
    def __init__(self, **kwargs):
        super(MyPS4Controller, self).__init__(**kwargs)
        self.left_velocity = 0
        self.right_velocity = 0

    def update_wheel_velocities(self):
        print('vl', self.left_velocity)
        print('vr', self.right_velocity)
        left_velocity = max(min(self.left_velocity, 500), -500)
        right_velocity = max(min(self.right_velocity, 500), -500)
        print(left_velocity, right_velocity)

    def on_L3_up(self, value):
        pass  # Ignore L3 up/down events

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        print('on_L3_left', (value / 32767) * 500)
        self.left_velocity += (value / 32767) * 500
        self.right_velocity -= (value / 32767) * 500
        self.update_wheel_velocities()

    def on_L3_right(self, value):
        print('on_L3_right', value)
        self.left_velocity -= value / 32767 * 500
        self.right_velocity += value / 32767 * 500
        self.update_wheel_velocities()

    def on_R2_press(self, value):
        print('on_R2_press', value)
        self.left_velocity = abs((value / 32767) * 500)
        self.right_velocity = abs((value / 32767) * 500)
        self.update_wheel_velocities()

    def on_L2_press(self, value):
        print('on_L2_press', (value / 32767) * 500)
        self.left_velocity = -1*abs((value / 32767) * 500)
        self.right_velocity = -1*abs((value / 32767) * 500)
        self.update_wheel_velocities()


controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
