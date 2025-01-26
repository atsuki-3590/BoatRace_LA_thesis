import pandas as pd
import pickle

STRAT_DATE = 20240611
END_DATE = 20240831

def predict_with_model(boat_number, custom_threshold):
    """
    指定されたボート番号に基づいて予測を行い、カスタム閾値を適用して結果を保存します。

    Parameters:
        boat_number (int): ボート番号（1〜6）
        custom_threshold (float): 予測確率の閾値
    """
    # データの読み込み
    data = pd.read_csv(f"betting_simulation\data\processed\modified_data{boat_number}_{STRAT_DATE}_{END_DATE}.csv")
    data['レース日'] = pd.to_datetime(data['レースコード'].str[:8], format='%Y%m%d')

    # モデルファイルのパスを組み立て
    model_path = f'models/boat{boat_number}_model_1.pkl'

    # モデルの読み込み
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    # 特徴量の準備（ターゲットカラム'3連複_結果'を除外）
    X = data.drop(columns=['レースコード', 'レース日', '3連複_結果'], errors='ignore')

    # 予測確率の計算
    y_pred_proba = model.predict_proba(X)[:, 1]

    # カスタム閾値を適用した予測
    data['predict_result'] = (y_pred_proba >= custom_threshold).astype(int)

    # 不要な列を削除
    data = data.drop('レース日', axis=1)

    # 予測結果を含んだデータの保存
    output_path = f"test_predictions_boat{boat_number}_{STRAT_DATE}_{END_DATE}.csv"
    data.to_csv(f"betting_simulation\data\processed\{output_path}", index=False)

    print(f"予測が完了し、結果が '{output_path}' に保存されました（ボート番号: {boat_number}, 閾値: {custom_threshold}）。")

# ボートごとのカスタム閾値を設定
boat_thresholds = {
    1: 0.5,
    2: 0.5,
    3: 0.5,
    4: 0.5,
    5: 0.5,
    6: 0.5,
}

# 全ボートで予測を実行
for boat_number, threshold in boat_thresholds.items():
    predict_with_model(boat_number, custom_threshold=threshold)
