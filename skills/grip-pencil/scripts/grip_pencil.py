import argparse
import sys
import time

sys.path.append('/home/pi/01/software')
from Arm_Lib import Arm_Device


def clamp(v):
    return max(0, min(180, int(round(v))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--open-angle', type=float, default=145)
    parser.add_argument('--close-angle', type=float, default=162)
    parser.add_argument('--wait-sec', type=float, default=2.0)
    parser.add_argument('--move-ms', type=int, default=500)
    args = parser.parse_args()

    open_angle = clamp(args.open_angle)
    close_angle = clamp(args.close_angle)

    arm = Arm_Device()
    arm.Arm_serial_servo_write(6, open_angle, args.move_ms)
    time.sleep(0.1)
    time.sleep(max(0.0, args.wait_sec))
    arm.Arm_serial_servo_write(6, close_angle, args.move_ms)
    time.sleep(0.1)


if __name__ == '__main__':
    main()
