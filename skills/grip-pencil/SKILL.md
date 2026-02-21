---
name: grip-pencil
description: ロボットアームのグリップを少し開いて2秒待ち、指定角度で閉じて鉛筆を掴む操作を行う。鉛筆を掴む/掴み直す指示が出たときに使う。
---

# Grip Pencil

## 概要

グリップ（サーボ6）だけを動かし、現在位置のまま鉛筆を掴む。
開く→待つ→閉じるの順で実行する（デフォルトの閉じ角度は162度）。

## 使い方

実行:
python /home/pi/01/software/skills/grip-pencil/scripts/grip_pencil.py

開き角度・閉じ角度・待ち時間・速度を指定:
python /home/pi/01/software/skills/grip-pencil/scripts/grip_pencil.py --open-angle 145 --close-angle 162 --wait-sec 2 --move-ms 500

## 注意

アームの位置は動かさず、グリップだけ動かす。鉛筆の位置は人が合わせておく。

## スクリプト

scripts/grip_pencil.py を使う。
