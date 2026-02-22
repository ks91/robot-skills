import time
import sys

sys.path.append("/home/pi/01/software")
from Arm_Lib import Arm_Device


def sleep_short():
    time.sleep(0.1)


def surprise(arm: Arm_Device):
    # Keep the grip horizontal: angle2 + angle3 + angle4 = 180.
    arm.Arm_serial_servo_write6(90, 100, 60, 20, 90, 180, 400)
    sleep_short()
    # Quick pull-back with horizontal grip.
    arm.Arm_serial_servo_write6(50, 180, 0, 0, 90, 180, 1100)
    sleep_short()
    # Slow return while keeping the grip horizontal.
    arm.Arm_serial_servo_write6(110, 120, 50, 10, 90, 180, 900)
    sleep_short()
    arm.Arm_serial_servo_write6(90, 100, 60, 20, 90, 180, 900)
    sleep_short()


def main():
    arm = Arm_Device()
    surprise(arm)


if __name__ == "__main__":
    main()
