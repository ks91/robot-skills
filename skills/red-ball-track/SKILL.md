---
name: red-ball-track
description: 手首カメラで赤いボールを検出し、画面中央に来るようにサーボ1/2を自動調整して追従する。赤ボール追跡や位置合わせをしたい時に使う。
---

# Red Ball Track

## これでできること

手首カメラ映像から赤色領域を検出し、対象が画面中央に近づくようにサーボ1（左右）とサーボ2（上下）を動かして追従する。  
開始時と終了時はカメラ確認用の姿勢に戻る。

## スクリプト

- メイン: `skills/red-ball-track/scripts/red_ball_tracker.py`
  - 実行時間上限: 45秒（`MAX_RUN_SEC`）
  - 追従対象: 最大の赤色領域（最小面積しきい値あり）
  - 制御対象: サーボ1（パン）・サーボ2（チルト）

## 使い方

1. 直接実行  
   `python skills/red-ball-track/scripts/red_ball_tracker.py`

2. 他のPythonから呼ぶ例  
   ```python
   import subprocess
   subprocess.run(
       ["python", "skills/red-ball-track/scripts/red_ball_tracker.py"],
       check=True,
   )
   ```

## 調整ポイント

- 追従が過敏/鈍い: `DEADBAND_PX`, `DEADBAND_Y` を調整。
- 小さいノイズを拾う: `MIN_AREA` を大きくする。
- 可動範囲を制限したい: `SERVO1_MIN/MAX`, `SERVO2_MIN/MAX` を調整。
- 追従速度を変えたい: ループ内のステップ計算（`step_x`, `step_y`）と書き込み時間を調整。
- 実行時間を伸ばす/短くする: `MAX_RUN_SEC` を変更。

## 安全メモ

- 実行前に可動域内の人・障害物を除去する。
- カメラが対象を見失った場合でも姿勢は保持されるため、停止時は周囲確認後に再実行する。
- 連続実行時はサーボ発熱に注意し、必要に応じて間隔を空ける。

