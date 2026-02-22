---
name: draw-circle
description: ロボットアームで円を描くスキル。今の先端位置を中心に、x距離をなるべく保ちながら円を描く。
---

# 使い方

今の先端位置を中心に、空中で円を描く。

実行:
python /home/pi/01/software/skills/draw-circle/draw_circle.py

半径指定（cm）:
python /home/pi/01/software/skills/draw-circle/draw_circle.py --radius-cm 10

滑らかさ（角度の間隔、数値が小さいほど滑らか）:
python /home/pi/01/software/skills/draw-circle/draw_circle.py --step-deg 8

速さ調整（数値を大きくするとゆっくり）:
python /home/pi/01/software/skills/draw-circle/draw_circle.py --move-ms 700
