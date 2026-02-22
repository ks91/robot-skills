---
name: arm-nod
description: Small, safe robot-arm nod motion. Use when the user asks for a nod/acknowledgement gesture, or when a brief, friendly nod reaction is needed during dialogue.
---

# Arm Nod

## Overview

Run a short, safe nod that returns to neutral. Keep the motion small and avoid large-range movement unless explicitly requested.

## Quick Start

Run the nod once:

```bash
python /home/pi/01/software/skills/arm-nod/scripts/nod.py
```

## Notes

- Keep motions small and slow (`duration >= 300` ms).
- Always return to neutral angles.
