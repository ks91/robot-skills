import time
import sys

sys.path.append("/home/pi/01/software")
from Arm_Lib import Arm_Device


def sleep_short():
    time.sleep(0.1)


def nod(arm: Arm_Device):
    # Set grip to a roughly horizontal pose before nodding.
    # angle2 + angle3 + angle4 - 180 = 0  -> 90 + 90 + 0 - 180 = 0
    arm.Arm_serial_servo_write6(90, 90, 90, 0, 90, 180, 800)
    sleep_short()
    # Small, safe nod around the horizontal pose.
    arm.Arm_serial_servo_write(2, 70, 600)
    sleep_short()
    arm.Arm_serial_servo_write(2, 110, 600)
    sleep_short()
    arm.Arm_serial_servo_write(2, 90, 600)
    sleep_short()


def main():
    arm = Arm_Device()
    nod(arm)


if __name__ == "__main__":
    main()
