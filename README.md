# robot-skills

This repository contains robot skills used in Academy Camp (https://academy-camp.org/).  
At the moment, it includes sample skills for the **Yahboom DOFBOT robotic arm**.

## Purpose

- Collect reusable motion scripts for classes and workshops
- Organize behavior in skill units that are easy to run and tune
- Provide a base that can later expand beyond DOFBOT

## Current Structure

```text
skills/
  arm-nod/              # Small nod/acknowledgement gesture
  arm-surprise/         # Short surprise reaction
  color-throw-4cm/      # Pick and softly throw an object around 4 cm
  draw-circle/          # Draw a circle in the air
  draw-square/          # Draw a square in the air
  draw-triangle/        # Draw a triangle in the air
  grip-pencil/          # Grip a pencil (gripper open/close)
  iya-iya/              # "No-no" side-to-side gesture
  red-ball-track/       # Track a red ball (camera + servo follow)
```

## Included Skills (DOFBOT)

| Skill | Summary | Docs | Run |
|---|---|---|---|
| `arm-nod` | Small, safe nod gesture that returns to neutral | `SKILL.md` available | `python skills/arm-nod/scripts/nod.py` |
| `arm-surprise` | Short surprise motion: quick pull-back, slow return | `SKILL.md` available | `python skills/arm-surprise/scripts/surprise.py` |
| `iya-iya` | Cute "no/no" side-to-side refusal gesture | `SKILL.md` available | `python skills/iya-iya/scripts/iya_iya.py` |
| `grip-pencil` | Open/close only the gripper (servo 6) to grip a pencil | `SKILL.md` available | `python skills/grip-pencil/scripts/grip_pencil.py` |
| `color-throw-4cm` | Pick an object (~4 cm) at the color-sorting position and softly throw it forward | `SKILL.md` available | `python skills/color-throw-4cm/scripts/color_throw_4cm.py` |
| `draw-circle` | Draw a circle in the air around the current tip position | `SKILL.md` available | `python skills/draw-circle/draw_circle.py` |
| `draw-square` | Draw a square in the air around the current tip position | `SKILL.md` available | `python skills/draw-square/draw_square.py` |
| `draw-triangle` | Draw an upward equilateral triangle in the air | `SKILL.md` available | `python skills/draw-triangle/draw_triangle.py` |
| `red-ball-track` | Detect a red object from the wrist camera and keep it centered using servo tracking | script only (`SKILL.md` not included) | `python skills/red-ball-track/scripts/red_ball_tracker.py` |

## Requirements

- Raspberry Pi environment connected to Yahboom DOFBOT
- Python 3
- `Arm_Lib` installed and importable
- For `red-ball-track`, also install `opencv-python` and `numpy`

## Basic Usage

1. Check safety around the robot (people, obstacles, movement range).
2. Read the skill's `SKILL.md` first, if available.
3. Run the Python script listed in the table above.
4. Tune angles, speed, and wait times for your actual hardware.

## Notes

- Included values (angles/timing) are sample values and may require adjustment per robot.
- Throwing motions require extra safety checks before execution.
- This repository currently targets DOFBOT and may not run as-is on other robots.

## Future Expansion

- Add new skills under `skills/<skill-name>/`
- Include a `SKILL.md` whenever possible (overview, usage, tuning, safety)
- If multi-robot support is added, consider a structure like `skills/<robot>/<skill-name>/`
