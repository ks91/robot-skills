import argparse
import math
import sys
import time

sys.path.append('/home/pi/01/software')
from Arm_Lib import Arm_Device

# Geometry (mm)
H_W = 6.0
H_B = 13.8
H_1 = 77.0
D_1 = 27.1
D_2 = 83.4
D_3 = 83.4
D_4 = 73.8
D_5_180 = 115.3


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


def r_z(a2, a3, a4):
    t2 = math.radians(a2)
    t23 = math.radians(a2 + a3 - 90)
    t234 = math.radians(a2 + a3 + a4 - 180)
    r = D_2 * math.cos(t2) + D_3 * math.cos(t23) + (D_4 + D_5_180) * math.cos(t234)
    z = H_W + H_B + H_1 + D_1 + (
        D_2 * math.sin(t2) + D_3 * math.sin(t23) + (D_4 + D_5_180) * math.sin(t234)
    )
    return r, z


def best_angles_for_rz(r_t, z_t, base_a2, base_a3):
    best = None
    for da2 in range(-50, 51, 5):
        a2c = clamp(base_a2 + da2)
        for da3 in range(-50, 51, 5):
            a3c = clamp(base_a3 + da3)
            a4c = 180 - a2c - a3c
            if not (0 <= a4c <= 180):
                continue
            r, z = r_z(a2c, a3c, a4c)
            cost = (r - r_t) ** 2 + (z - z_t) ** 2
            if best is None or cost < best[0]:
                best = (cost, a2c, a3c)
    _, b2, b3 = best
    best = None
    for da2 in range(-8, 9, 1):
        a2c = clamp(b2 + da2)
        for da3 in range(-8, 9, 1):
            a3c = clamp(b3 + da3)
            a4c = 180 - a2c - a3c
            if not (0 <= a4c <= 180):
                continue
            r, z = r_z(a2c, a3c, a4c)
            cost = (r - r_t) ** 2 + (z - z_t) ** 2
            if best is None or cost < best[0]:
                best = (cost, a2c, a3c)
    a2b, a3b = best[1], best[2]
    return a2b, a3b, 180 - a2b - a3b


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size-cm', type=float, default=6.8)
    parser.add_argument('--move-ms', type=int, default=400)
    args = parser.parse_args()

    arm = Arm_Device()
    arm.Arm_serial_set_torque(1)
    angles = [read_angle(arm, i) for i in range(1, 7)]
    a1, a2, a3, a4, a5, a6 = angles

    # Common start pose: face forward + horizontal grip
    start_pose = [90, 60, 60, 60, 90, a6]
    arm.Arm_serial_servo_write6_array(start_pose, args.move_ms + 200)
    time.sleep(0.1)
    angles = start_pose
    a1, a2, a3, a4, a5, a6 = angles

    r0, z0 = r_z(a2, a3, a4)
    r0 = max(1.0, r0)
    rad_a1 = math.radians(a1)
    x0 = r0 * math.sin(rad_a1)
    y0 = r0 * math.cos(rad_a1)

    side = args.size_cm * 10.0
    half = side / 2.0

    corners = [
        (y0 - half, z0 - half),
        (y0 + half, z0 - half),
        (y0 + half, z0 + half),
        (y0 - half, z0 + half),
        (y0 - half, z0 - half),
    ]

    path = []
    cur_a2, cur_a3 = a2, a3
    for y_t, z_t in corners:
        r_t = math.hypot(x0, y_t)
        a2c, a3c, a4c = best_angles_for_rz(r_t, z_t, cur_a2, cur_a3)
        a1c = math.degrees(math.atan2(x0, y_t))
        a1c = clamp(a1c)
        path.append([a1c, a2c, a3c, a4c, a5, a6])
        cur_a2, cur_a3 = a2c, a3c

    # move to first point
    start = angles
    first = path[0]
    for i in range(1, 7):
        interp = [int(round(start[j] + (first[j] - start[j]) * i / 6)) for j in range(6)]
        arm.Arm_serial_servo_write6_array(interp, args.move_ms + 50)
        time.sleep(0.1)

    # draw
    seg_steps = 12
    for i in range(len(path) - 1):
        p0 = path[i]
        p1 = path[i + 1]
        for s in range(1, seg_steps + 1):
            interp = [int(round(p0[j] + (p1[j] - p0[j]) * s / seg_steps)) for j in range(6)]
            arm.Arm_serial_servo_write6_array(interp, args.move_ms)
            time.sleep(0.1)


if __name__ == '__main__':
    main()
