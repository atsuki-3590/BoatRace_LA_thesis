# 作成したモデルから、予測結果を含んだデータの保存
import pandas as pd
import pickle

STRAT_DATE = 20240611
END_DATE = 20240731

def predict_with_model(boat_number):
    # データの読み込み
    data = pd.read_csv(f"betting_simulation\data\processed\modified_data{boat_number}_{STRAT_DATE}_{END_DATE}.csv")
    data['レース日'] = pd.to_datetime(data['レースコード'].str[:8], format='%Y%m%d')

    # 後ろ2割の抽出を削除し、全データを使用
    # 日付範囲によるフィルタリングが必要であれば以下を有効化
    # data = data[data['レース日'] >= pd.Timestamp('2024-06-11')]

    # モデルファイルのパスを組み立て
    model_path = f'models/boat{boat_number}_model_1.pkl'

    # モデルの読み込み
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    # 特徴量の準備（ターゲットカラム'3連複_結果'を除外）
    X = data.drop(columns=['レースコード', 'レース日', '3連複_結果'], errors='ignore')

    # 予測の実行
    data['predict_result'] = model.predict(X)

    # 不要な列を削除
    data = data.drop('レース日', axis=1)

    # 予測結果を含んだデータの保存
    output_path = f"test_predictions_boat{boat_number}_{STRAT_DATE}_{END_DATE}.csv"
    data.to_csv(f"betting_simulation\data\processed\{output_path}", index=False)

    print(f"予測が完了し、結果が '{output_path}' に保存されました。")

# 全ボートで予測を実行
for i in range(1, 7):
    predict_with_model(i)



