---
name: draw-square
description: ロボットアームで正方形を描くスキル。今の先端位置を中心に、x距離をなるべく保ちながら四角を描く。
---

# 使い方

今の先端位置を中心に、空中で正方形を描く。

実行:
python /home/pi/01/software/skills/draw-square/draw_square.py

大きさ指定（1辺cm）:
python /home/pi/01/software/skills/draw-square/draw_square.py --size-cm 5

速さ調整（数値を大きくするとゆっくり）:
python /home/pi/01/software/skills/draw-square/draw_square.py --move-ms 600
