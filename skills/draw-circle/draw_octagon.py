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


def fk_xyz(a1, a2, a3, a4):
    t1 = math.radians(a1)
    t2 = math.radians(a2)
    t23 = math.radians(a2 + a3 - 90)
    t234 = math.radians(a2 + a3 + a4 - 180)
    r = D_2 * math.cos(t2) + D_3 * math.cos(t23) + (D_4 + D_5_180) * math.cos(t234)
    z = H_W + H_B + H_1 + D_1 + (
        D_2 * math.sin(t2) + D_3 * math.sin(t23) + (D_4 + D_5_180) * math.sin(t234)
    )
    x = r * math.sin(t1)
    y = r * math.cos(t1)
    return x, y, z


def solve_a2a3a4(x_t, y_t, z_t, base_a2, base_a3, base_a4):
    best = None
    # coarse search
    for a2 in range(30, 151, 6):
        for a3 in range(30, 151, 6):
            for a4 in range(30, 151, 6):
                x, y, z = fk_xyz(90, a2, a3, a4)
                dx = x - x_t
                dy = y - y_t
                dz = z - z_t
                cost = dx*dx + dy*dy + dz*dz
                if best is None or cost < best[0]:
                    best = (cost, a2, a3, a4)
    _, b2, b3, b4 = best
    # refine around best
    best = None
    for a2 in range(max(0, b2 - 8), min(180, b2 + 8) + 1, 1):
        for a3 in range(max(0, b3 - 8), min(180, b3 + 8) + 1, 1):
            for a4 in range(max(0, b4 - 8), min(180, b4 + 8) + 1, 1):
                x, y, z = fk_xyz(90, a2, a3, a4)
                dx = x - x_t
                dy = y - y_t
                dz = z - z_t
                cost = dx*dx + dy*dy + dz*dz
                if best is None or cost < best[0]:
                    best = (cost, a2, a3, a4)
    return best[1], best[2], best[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--x-mm', type=float, default=200.0)
    parser.add_argument('--radius-cm', type=float, default=5.6)
    parser.add_argument('--move-ms', type=int, default=180)
    parser.add_argument('--start-ms', type=int, default=600)
    parser.add_argument('--wait-sec', type=float, default=0.0)
    args = parser.parse_args()

    arm = Arm_Device()
    arm.Arm_serial_set_torque(1)

    # fixed start pose (always start from the same position)
    a6 = read_angle(arm, 6, 180)
    start_pose = [90, 118, 25, 35, 90, a6]
    start_ms = max(600, int(args.start_ms))
    # send twice to guarantee the move is taken before drawing
    arm.Arm_serial_servo_write6_array(start_pose, start_ms)
    time.sleep(start_ms / 1000.0 + 0.05)
    arm.Arm_serial_servo_write6_array(start_pose, start_ms)
    time.sleep(start_ms / 1000.0 + 0.05)
    # no extra wait by default (start drawing immediately)
    if args.wait_sec > 0:
        time.sleep(args.wait_sec)

    # center based on the start pose (start point is the top vertex)

    # polygon vertices on plane x=x0
    x0 = 200.0
    y0 = 0.0
    radius = args.radius_cm * 10.0
    z0 = fk_xyz(90, 118, 25, 35)[2] - radius + 20.0
    points = []
    sides = 16
    for i in range(sides + 1):
        th = math.radians(90 - i * (360.0 / sides))
        y = y0 + radius * math.cos(th)
        z = z0 + radius * math.sin(th)
        points.append((x0, y, z))

    path = []
    base_a2, base_a3, base_a4 = 60, 60, 60
    for x_t, y_t, z_t in points:
        # a1 from x,y target
        a1c = clamp(math.degrees(math.atan2(x_t, y_t if abs(y_t) > 1e-6 else 1e-6)))
        a2c, a3c, a4c = solve_a2a3a4(x_t, y_t, z_t, base_a2, base_a3, base_a4)
        path.append([a1c, a2c, a3c, a4c, 90, a6])
        base_a2, base_a3, base_a4 = a2c, a3c, a4c

    # draw (start from the horizontal pose without extra lift)
    for s in path:
        arm.Arm_serial_servo_write6_array(s, args.move_ms)
        time.sleep(args.move_ms / 1000.0 + 0.02)


if __name__ == '__main__':
    main()
