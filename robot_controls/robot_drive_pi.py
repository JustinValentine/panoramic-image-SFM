import time
from ds4drv.backends import get_backend
from ds4drv.controllers import BaseController


class MyPS4Controller(BaseController):
    def __init__(self, interface="/dev/input/js0", connecting_using_ds4drv=False):
        backend = get_backend(connecting_using_ds4drv)
        super(MyPS4Controller, self).__init__(backend, interface)


def handle_axes_event(event):
    left_velocity = 0
    right_velocity = 0

    # L3 to turn
    if event.axis == BaseController.Axes.LEFT_ANALOG_X:
        turn_speed = event.value  # Assuming event.value is in the range of -1 to 1
        left_velocity += turn_speed
        right_velocity -= turn_speed

    # R2 to move forward
    if event.axis == BaseController.Axes.RIGHT_TRIGGER:
        forward_speed = event.value  # Assuming event.value is in the range of 0 to 1
        left_velocity += forward_speed
        right_velocity += forward_speed

    # L2 to move back
    if event.axis == BaseController.Axes.LEFT_TRIGGER:
        backward_speed = -event.value  # Assuming event.value is in the range of 0 to 1
        left_velocity += backward_speed
        right_velocity += backward_speed

    print(left_velocity, right_velocity)

controller = MyPS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.on_axes_event = handle_axes_event

controller.start()
time.sleep(0.1)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    controller.stop()
