# BoatRace_LA_thesis
教養卒論用のボートレース予測モデル
データ数を変更する際は、data/rawファイル内に以下のファイルを用意
- info.csv（出走表データ）
- result.csv（結果データ）
- odds_3f.csv（3連複オッズデータ）



### 生データの編集
1. 出走表データ（info.csv）と結果データ（result.csv）を結合してmerged_data.csvに（scripts\data_marged.py）

2. データ内の予想に必要ないデータ（選手名や登録番号など）を削除し、枠番ごとのデータを作成。特徴量エンジニアリング（勝率などのZスコア変換や風向の変換など）もここで行う（merged_dataからdata_boat1.csvを作成）。（scripts\preprocessing_by_course.py）


### モデルの訓練（コースごと）
<!-- 以下は現在コースごとだが、関数化してまとめる予定 -->
3. 予想に必要な特徴量を選定（data_boat1.csvからmodified_data1.csvを作成）。（scripts_by_course\boat1\data_preprocessing.py（scripts\data_preprocessing.pyは全体をまとめて処理したいとき））

4. 訓練モデルをトレーニング（scripts_by_course\boat1\train_model.py）


### 検証
5. データの一部を検証用に用いる、訓練されたモデルを用いて予測データを作成（scrpits_verification\save_predictions_with_model.py）

6. 予測データと結果データ、オッズデータを結合する（scrpits_verification\test_data_marged.py）

7. 作成されたデータをもとに、回収率を計算する（scrpits_verification\betting_analysis.py）

