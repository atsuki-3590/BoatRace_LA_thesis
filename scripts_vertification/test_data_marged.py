# 予測データと結果データ、オッズデータを結合するスクリプト
import pandas as pd
from functools import reduce

# 予測データ
file_paths = [
    'data/processed/test_predictions_boat1.csv',
    'data/processed/test_predictions_boat2.csv',
    'data/processed/test_predictions_boat3.csv',
    'data/processed/test_predictions_boat4.csv',
    'data/processed/test_predictions_boat5.csv',
    'data/processed/test_predictions_boat6.csv'
]

# 結果データ
result_file_paths = [
    'data/processed/data_boat1.csv',
    'data/processed/data_boat2.csv',
    'data/processed/data_boat3.csv',
    'data/processed/data_boat4.csv',
    'data/processed/data_boat5.csv',
    'data/processed/data_boat6.csv'
]

# Predictions データの結合
data_frames = []
for idx, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path)
    df = df[['レースコード', 'predict_result']].rename(columns={'predict_result': f'predict_result_{idx}'})
    data_frames.append(df)

predictions_df = reduce(lambda left, right: pd.merge(left, right, on='レースコード', how='outer'), data_frames)

# Results データの結合
result_data_frames = []
for idx, file_path in enumerate(result_file_paths, start=1):
    df = pd.read_csv(file_path)
    df = df[['レースコード', '3連複_結果']].rename(columns={'3連複_結果': f'result_{idx}'})
    result_data_frames.append(df)

results_df = reduce(lambda left, right: pd.merge(left, right, on='レースコード', how='outer'), result_data_frames)

# Predictions と Results の結合
predictions_df = pd.merge(predictions_df, results_df, on='レースコード', how='inner')

# オッズデータの追加
odds_data = pd.read_csv('data/raw/odds_3f_new.csv')
final_df = pd.merge(predictions_df, odds_data, on='レースコード', how='inner')

result_columns = [f'result_{i}' for i in range(1, 7)]
final_df['result'] = final_df[result_columns].apply(lambda row: '='.join([str(i+1) for i, val in enumerate(row) if val == 1]), axis=1)

final_df.drop(columns=result_columns, inplace=True)

output_path = "test_predict_with_odds.csv"
final_df.to_csv(f"data/processed/{output_path}", index=False)

# 結果を確認
print(final_df.head())