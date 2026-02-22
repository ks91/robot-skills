---
name: draw-triangle
description: ロボットアームで上向きの正三角形を描くスキル。今の先端位置を中心に、x距離をなるべく保ちながら三角形を描く。
---

# 使い方

今の先端位置を中心に、空中で正三角形を描く。

実行:
python /home/pi/01/software/skills/draw-triangle/draw_triangle.py

大きさ指定（1辺cm）:
python /home/pi/01/software/skills/draw-triangle/draw_triangle.py --size-cm 5

速さ調整（数値を大きくするとゆっくり）:
python /home/pi/01/software/skills/draw-triangle/draw_triangle.py --move-ms 600
