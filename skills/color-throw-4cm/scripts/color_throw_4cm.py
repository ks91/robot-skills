#!/usr/bin/env python3
"""Grab a 4cm block at the color-sorting object spot and gently toss it forward."""
import sys
import time
from pathlib import Path

# Allow running from anywhere by adding project root to sys.path.
BASE_DIR = Path(__file__).resolve().parents[3]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from Arm_Lib import Arm_Device


Arm = Arm_Device()

# Angles for the first five joints; gripper is appended per move.
HOME = [90, 90, 90, 90, 90]
OBJECT_POS = [90, 43, 36, 40, 90]  # "Position for grabbing the colored box"
LIFT_AFTER_GRAB = [90, 80, 35, 40, 90]
# Toss sequence angles
DIP_BEFORE_THROW = [90, 70, 30, 35, 90]  # slight dip to preload before swing
UP_THROW = [90, 118, 72, 82, 90]  # high upward arc (shoulder back to avoid ground hit)
FORWARD_SWING_LATE = [90, 98, 58, 62, 90]  # continue after release with arm still above ground
FOLLOW_THROUGH = [90, 70, 70, 80, 90]  # slow down safely

GRIP_4CM = 125  # slightly tighter than table to ensure hold
OPEN_WIDE = 30
RELEASE_OPEN = 70  # open wider to release earlier in arc

# Timing (ms) for key motions
DUR_PICK = 900
DUR_LIFT = 850
DUR_UP_THROW = 220  # slower upswing so release happens later (for backward throw)
DUR_FORWARD_SWING_LATE = 200
DUR_RELEASE = 30
DUR_FOLLOW = 550
DUR_HOME = 900
DUR_DIP = 350


def move(joints, gripper, duration=800, pause=0.12):
    """Move all servos together and wait for completion."""
    Arm.Arm_serial_servo_write6_array(joints + [gripper], duration)
    time.sleep(duration / 1000 + pause)


def set_gripper(angle, duration=400, pause=0.12):
    """Move only the gripper servo."""
    Arm.Arm_serial_servo_write(6, angle, duration)
    time.sleep(duration / 1000 + pause)


def toss_4cm_block():
    """Pick a 4cm block at the object position and lightly toss it forward."""
    move(HOME, gripper=RELEASE_OPEN, duration=DUR_HOME, pause=0.2)

    # Approach and grab
    move(OBJECT_POS, gripper=OPEN_WIDE, duration=DUR_PICK, pause=0.2)
    set_gripper(GRIP_4CM, duration=650, pause=0.2)
    move(LIFT_AFTER_GRAB, gripper=GRIP_4CM, duration=DUR_LIFT, pause=0.18)
    move(DIP_BEFORE_THROW, gripper=GRIP_4CM, duration=DUR_DIP, pause=0.12)

    # Gentle toss sequence: dip, then upswing and release slightly later (for backward toss)
    move(UP_THROW, gripper=GRIP_4CM, duration=DUR_UP_THROW, pause=0.04)
    set_gripper(RELEASE_OPEN, duration=DUR_RELEASE, pause=0.04)
    move(FORWARD_SWING_LATE, gripper=RELEASE_OPEN, duration=DUR_FORWARD_SWING_LATE, pause=0.12)
    move(FOLLOW_THROUGH, gripper=RELEASE_OPEN, duration=DUR_FOLLOW, pause=0.16)

    # Return to a safe resting pose
    move(HOME, gripper=RELEASE_OPEN, duration=DUR_HOME, pause=0.2)
    return "done"


if __name__ == "__main__":
    toss_4cm_block()
