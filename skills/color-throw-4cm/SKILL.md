---
name: color-throw-4cm
description: 色仕分けゲームで、オブジェクトポジションにある4cm程度の箱/ブロックを掴んで前方に軽く投げる。色仕分けの掴み位置から4cm物体を拾い、前方へソフトスローしたい時に使う。
---

# Color Throw 4cm

## これでできること
色仕分けの「オブジェクトのポジション」([90, 43, 36, 40, 90]) にある約4cmの物体をグリッパー115度で掴み、少し後ろにためてから前方へ軽くスイングして放す。投げ終わったら安全な姿勢(HOME)に戻す。

## スクリプト
- メイン: `software/skills/color-throw-4cm/scripts/color_throw_4cm.py`
  - 掴む時: グリッパー 115度 (4cm用)
  - 投げる時: リリース 40度で軽く開放
  - ポーズ: READY→LIFT→PRE_THROW→FORWARD_SWING→FOLLOW→HOME

## 使い方
1. 直接実行  
   `python software/skills/color-throw-4cm/scripts/color_throw_4cm.py`

2. 他のPythonから呼ぶ例  
   ```python
   import subprocess
   subprocess.run(
       ["python", "software/skills/color-throw-4cm/scripts/color_throw_4cm.py"],
       check=True,
   )
   ```

## 調整ポイント
- 掴みが緩い/きつい: `GRIP_4CM` を115から前後させる (表の目安に従う)。
- 投げ距離を伸ばす: `FORWARD_SWING` の肩/肘角度を少し小さめにし、`duration` を短くする。ただし急激にしすぎない。
- 投げを弱める: `PRE_THROW` を小さく、`FORWARD_SWING` の duration を長めにする。
- 離すタイミングを変える: `RELEASE_OPEN` の角度やリリース前後の `duration` を微調整。

## 安全メモ
- 周囲に人や障害物がないか確認してから実行。
- 4cmより大きい/小さい物体はグリッパ角度を必ず調整してから使う。
- 同じ動作を連続するときは0.5秒以上あけるとサーボの取りこぼしを防ぎやすい。
