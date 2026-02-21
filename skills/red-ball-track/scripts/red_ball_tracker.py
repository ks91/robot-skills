#!/usr/bin/env python3
"""Track a red ball with the wrist camera and steer servo1 to keep it centered."""
import time
from pathlib import Path

import cv2
import numpy as np

# Allow running from anywhere by adding project root to sys.path.
import sys

BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from Arm_Lib import Arm_Device


Arm = Arm_Device()

# Camera settings
FRAME_W = 640
FRAME_H = 480
DEADBAND_PX = 30  # no servo correction if within this distance from center
DEADBAND_Y = 28
MIN_AREA = 250  # ignore tiny red blobs
MAX_RUN_SEC = 45

# Initial pose facing forward for color checking (gripper slightly open)
CAM_POSE = [90, 120, 0, 0, 90, 30]
SERVO1_MIN = 30
SERVO1_MAX = 150
SERVO2_MIN = 40
SERVO2_MAX = 140
SERVO2_MIN = 40
SERVO2_MAX = 140


def clamp(val, low, high):
    return max(low, min(high, val))


def setup_camera():
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc("M", "J", "P", "G"))
    cam.set(cv2.CAP_PROP_BRIGHTNESS, 30)
    cam.set(cv2.CAP_PROP_CONTRAST, 50)
    return cam


def find_red_center(frame):
    """Return (cx, cy, area) of the largest red blob, or (None, None, 0)."""
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # Red wraps HSV hue, so combine two ranges
    lower1 = np.array([0, 120, 70])
    upper1 = np.array([10, 255, 255])
    lower2 = np.array([170, 120, 70])
    upper2 = np.array([180, 255, 255])
    mask = cv2.inRange(hsv, lower1, upper1) | cv2.inRange(hsv, lower2, upper2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, 0
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    if area < MIN_AREA:
        return None, None, 0
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return None, None, 0
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return cx, cy, area


def move_pose(pose, duration=800, pause=0.15):
    Arm.Arm_serial_servo_write6_array(pose, duration)
    time.sleep(duration / 1000 + pause)


def main():
    # Start at camera-forward pose
    move_pose(CAM_POSE, duration=800, pause=0.25)
    cam = setup_camera()
    center_x = FRAME_W // 2
    center_y = FRAME_H // 2
    servo1 = CAM_POSE[0]
    servo2 = CAM_POSE[1]
    start = time.time()
    print("tracking_start")
    try:
        while time.time() - start < MAX_RUN_SEC:
            # Clear buffer then read
            cam.read()
            ret, frame = cam.read()
            if not ret:
                print("frame_read_fail")
                time.sleep(0.2)
                continue

            cx, cy, area = find_red_center(frame)
            if cx is None:
                time.sleep(0.08)
                continue

            error_x = cx - center_x
            error_y = cy - center_y

            step_x = 0
            step_y = 0

            if abs(error_x) >= DEADBAND_PX:
                step_x = clamp(int(abs(error_x) / 25), 3, 7)
                # If target is left, turn left (increase angle); if right, turn right.
                if error_x < 0:
                    servo1 += step_x
                else:
                    servo1 -= step_x
                servo1 = clamp(servo1, SERVO1_MIN, SERVO1_MAX)

            if abs(error_y) >= DEADBAND_Y:
                step_y = clamp(int(abs(error_y) / 25), 2, 6)
                # Invert direction: if target is higher (smaller y), tilt down (increase servo2); if lower, tilt up.
                if error_y < 0:
                    servo2 += step_y
                else:
                    servo2 -= step_y
                servo2 = clamp(servo2, SERVO2_MIN, SERVO2_MAX)

            if step_x == 0 and step_y == 0:
                time.sleep(0.05)
                continue

            Arm.Arm_serial_servo_write6_array(
                [servo1, servo2, CAM_POSE[2], CAM_POSE[3], CAM_POSE[4], CAM_POSE[5]], 220
            )
            time.sleep(0.12)
    except KeyboardInterrupt:
        print("stopped_by_user")
    finally:
        cam.release()
        move_pose(CAM_POSE, duration=800, pause=0.2)
        print("tracking_end")


if __name__ == "__main__":
    main()
