import time
from pyPS4Controller.controller import Controller

class MyPS4Controller(Controller):
    def __init__(self, **kwargs):
        super(MyPS4Controller, self).__init__(**kwargs)
        self.left_velocity = 0
        self.right_velocity = 0

    def on_L3_up(self, value):
        pass  # Ignore L3 up/down events

    def on_L3_down(self, value):
        pass

    def on_L3_left(self, value):
        self.left_velocity += value / 32767
        self.right_velocity -= value / 32767
        print(self.left_velocity, self.right_velocity)

    def on_L3_right(self, value):
        self.left_velocity -= value / 32767
        self.right_velocity += value / 32767
        print(self.left_velocity, self.right_velocity)

    def on_R2_press(self, value):
        self.left_velocity += value / 255
        self.right_velocity += value / 255
        print(self.left_velocity, self.right_velocity)

    def on_L2_press(self, value):
        self.left_velocity -= value / 255
        self.right_velocity -= value / 255
        print(self.left_velocity, self.right_velocity)


controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
