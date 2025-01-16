import pandas as pd
import os

STRAT_DATE = 20240611
END_DATE = 20240831

# ファイルのパス
info_path = f'betting_simulation/data/raw/info_{STRAT_DATE}_{END_DATE}.csv'
result_path = f'betting_simulation/data/raw/result_{STRAT_DATE}_{END_DATE}.csv'

# CSVファイルの読み込み（エンコーディングをshift-jisに指定）
info_df = pd.read_csv(info_path, encoding='UTF-8')
result_df = pd.read_csv(result_path, encoding='UTF-8', low_memory=False)

# "レースコード"で結合（左外部結合）
merged_df = pd.merge(info_df, result_df, on='レースコード', how='left', suffixes=('', '_result'))

# 重複したカラムを処理（result_dfのカラムを優先）
for column in merged_df.columns:
    if column.endswith('_result'):
        original_column = column.replace('_result', '')
        if original_column in merged_df.columns:
            merged_df[original_column] = merged_df[column]
            merged_df.drop([column], axis=1, inplace=True)

# カラムの順番を指定
columns_order = ['レースコード'] + [col for col in merged_df.columns if col != 'レースコード']
merged_df = merged_df[columns_order]

# 出力パスを指定
output_path = f'betting_simulation/data/raw/merged_data_{STRAT_DATE}_{END_DATE}.csv'

# 出力先のディレクトリが存在しない場合は作成
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# CSVファイルをUTF-8で保存
merged_df.to_csv(output_path, index=False, encoding='utf-8')

print("データの結合が完了し、UTF-8形式で保存されました。")
