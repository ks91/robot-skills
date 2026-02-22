import subprocess
import sys


def main():
    # Delegate to the canonical circle behavior so every context matches.
    args = [sys.executable, '/home/pi/01/software/skills/draw-circle/draw_octagon.py']
    args.extend(sys.argv[1:])
    raise SystemExit(subprocess.call(args))


if __name__ == '__main__':
    main()
