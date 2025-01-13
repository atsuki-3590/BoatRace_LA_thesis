# 作成したモデルから、予測結果を含んだデータの保存
import pandas as pd
import pickle

def predict_with_model(boat_number):
    # データの読み込み
    data = pd.read_csv(f"data\processed\modified_data{boat_number}.csv")
    data['レース日'] = pd.to_datetime(data['レースコード'].str[:8], format='%Y%m%d')
    data = data[data['レース日'] >= pd.Timestamp('2024-06-01')]


    # モデルファイルのパスを組み立て
    model_path = f'models/boat{boat_number}_model_1.pkl'

    # モデルの読み込み
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

    # 特徴量の準備（ターゲットカラム'3連複_結果'を除外）
    X = data.drop(columns=['レースコード', 'レース日', '3連複_結果'], errors='ignore')

    # 予測の実行
    data['predict_result'] = model.predict(X)

    data = data.drop('レース日', axis=1)

    # 予測結果を含んだデータの保存
    output_path = f"test_predictions_boat{boat_number}.csv"
    data.to_csv(f"data\processed\{output_path}", index=False)

    print(f"予測が完了し、結果が '{output_path}' に保存されました。")

# 使用例: boat1 のモデルを使って予測
# predict_with_model(1)

for i in range(1, 7):
    predict_with_model(i)




