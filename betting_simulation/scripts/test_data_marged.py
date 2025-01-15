import pandas as pd
from functools import reduce

STRAT_DATE = 20240611
END_DATE = 20240731  # 修正：データ範囲を2024年6月30日までに変更
END_DATE_filepath = 20240731  # 修正：ファイル名に含めるデータ範囲を2024年7月31日までに変更

# 日付範囲を整数で定義
START_DATE_INT = int(STRAT_DATE)
END_DATE_INT = int(END_DATE)

# 予測データ
file_paths = [
    f'betting_simulation/data/processed/test_predictions_boat1_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/test_predictions_boat2_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/test_predictions_boat3_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/test_predictions_boat4_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/test_predictions_boat5_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/test_predictions_boat6_{STRAT_DATE}_{END_DATE_filepath}.csv'
]

# 結果データ
result_file_paths = [
    f'betting_simulation/data/processed/data_boat1_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/data_boat2_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/data_boat3_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/data_boat4_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/data_boat5_{STRAT_DATE}_{END_DATE_filepath}.csv',
    f'betting_simulation/data/processed/data_boat6_{STRAT_DATE}_{END_DATE_filepath}.csv',
]

# レースコードから日付を抽出する関数
def extract_date_from_code(race_code):
    return int(race_code[:8])

# Predictions データの結合
data_frames = []
for idx, file_path in enumerate(file_paths, start=1):
    df = pd.read_csv(file_path)
    df['レース日'] = df['レースコード'].apply(extract_date_from_code)  # 日付を抽出
    df = df[(df['レース日'] >= START_DATE_INT) & (df['レース日'] <= END_DATE_INT)]  # 日付でフィルタリング
    df = df[['レースコード', 'レース日', 'predict_result']].rename(columns={'predict_result': f'predict_result_{idx}'})
    data_frames.append(df)

predictions_df = reduce(lambda left, right: pd.merge(left, right, on=['レースコード', 'レース日'], how='outer'), data_frames)

# Results データの結合
result_data_frames = []
for idx, file_path in enumerate(result_file_paths, start=1):
    df = pd.read_csv(file_path)
    df['レース日'] = df['レースコード'].apply(extract_date_from_code)  # 日付を抽出
    df = df[(df['レース日'] >= START_DATE_INT) & (df['レース日'] <= END_DATE_INT)]  # 日付でフィルタリング
    df = df[['レースコード', 'レース日', '3連複_結果']].rename(columns={'3連複_結果': f'result_{idx}'})
    result_data_frames.append(df)

results_df = reduce(lambda left, right: pd.merge(left, right, on=['レースコード', 'レース日'], how='outer'), result_data_frames)

# Predictions と Results の結合
predictions_df = pd.merge(predictions_df, results_df, on=['レースコード', 'レース日'], how='inner')

# オッズデータの追加
odds_data = pd.read_csv('betting_simulation/data/raw/odds_3f_20240611_20240731.csv')
odds_data['レース日'] = odds_data['レースコード'].apply(extract_date_from_code)  # 日付を抽出
odds_data = odds_data[(odds_data['レース日'] >= START_DATE_INT) & (odds_data['レース日'] <= END_DATE_INT)]  # 日付でフィルタリング
final_df = pd.merge(predictions_df, odds_data, on=['レースコード', 'レース日'], how='inner')

# 結果列の生成
result_columns = [f'result_{i}' for i in range(1, 7)]
final_df['result'] = final_df[result_columns].apply(lambda row: '='.join([str(i+1) for i, val in enumerate(row) if val == 1]), axis=1)

final_df.drop(columns=result_columns, inplace=True)

# ファイル出力
output_path = f"test_predict_with_odds_{STRAT_DATE}_{END_DATE}.csv"
final_df.to_csv(f"betting_simulation/data/processed/{output_path}", index=False)

# 結果を確認
print(final_df.head())