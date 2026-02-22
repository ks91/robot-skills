import argparse
import sys
import time

sys.path.append('/home/pi/01/software')
from Arm_Lib import Arm_Device


def clamp(v):
    return max(0, min(180, int(round(v))))


def read_angle(arm, i, default=90):
    try:
        v = arm.Arm_serial_servo_read(i)
        if v is None:
            return default
        return int(v)
    except Exception:
        return default


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--swing-deg', type=int, default=20)
    parser.add_argument('--cycles', type=int, default=3)
    parser.add_argument('--move-ms', type=int, default=250)
    parser.add_argument('--pause-ms', type=int, default=80)
    args = parser.parse_args()

    arm = Arm_Device()
    arm.Arm_serial_set_torque(1)

    angles = [read_angle(arm, i) for i in range(1, 7)]
    a1, a2, a3, a4, a5, a6 = angles

    swing = max(5, min(70, args.swing_deg))
    left = clamp(a1 - swing)
    right = clamp(a1 + swing)

    # Small wrist tilt to make the motion feel more expressive
    w_left = clamp(a5 + 12)
    w_right = clamp(a5 - 12)

    # Center first to avoid sudden jump
    arm.Arm_serial_servo_write6_array([a1, a2, a3, a4, a5, a6], args.move_ms)
    time.sleep(0.1)

    for _ in range(max(1, args.cycles)):
        arm.Arm_serial_servo_write6_array([left, a2, a3, a4, w_left, a6], args.move_ms)
        time.sleep(max(0.01, args.pause_ms / 1000.0))
        arm.Arm_serial_servo_write6_array([right, a2, a3, a4, w_right, a6], args.move_ms)
        time.sleep(max(0.01, args.pause_ms / 1000.0))

    # Return to original pose
    arm.Arm_serial_servo_write6_array([a1, a2, a3, a4, a5, a6], args.move_ms + 50)
    time.sleep(0.1)


if __name__ == '__main__':
    main()
