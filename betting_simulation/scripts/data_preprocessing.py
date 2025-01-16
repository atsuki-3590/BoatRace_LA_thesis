import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# データ前処理

STRAT_DATE = 20240611
END_DATE = 20240831


def preprocess_boat_data(boat_number):
    print(f"データ前処理を開始します ({boat_number}号艇)")

    # ディレクトリの設定
    processed_dir = 'betting_simulation/data/processed/'
    
    # ファイルパスを生成
    input_file_path = f"{processed_dir}data_boat{boat_number}_{STRAT_DATE}_{END_DATE}.csv"
    output_file_path = f"{processed_dir}modified_data{boat_number}_{STRAT_DATE}_{END_DATE}.csv"

    # データの読み込み
    df = pd.read_csv(input_file_path, low_memory=False)

    # 削除する列を指定
    columns_to_drop = [
        '枠', '順位', '結果', '天気', '体重',
        # 'レース場', 
        '全国勝率', '全国2連対率', 'モーター2連対率', 'ボート2連対率', 
        # '当地2連対率', '当地勝率', '全国2連対率_Zスコア', '当地2連対率_Zスコア', '展示タイム'
        '当地2連対率', '当地勝率', '展示タイム'
    ]

    # 指定した列を削除
    new_data = df.drop(columns=columns_to_drop)

    # 欠損値の確認
    missing_values = new_data.isnull().sum()
    print(f"欠損値の確認:\n{missing_values}")

    # カテゴリカルデータの確認
    categorical_columns = new_data.select_dtypes(include=['object']).columns
    if 'レースコード' in categorical_columns:
        categorical_columns = categorical_columns.drop('レースコード')

    # 欠損値を含む行を削除
    data_filtered = new_data.dropna()

    # カテゴリカルデータのラベルエンコーディング
    for column in categorical_columns:
        if column in data_filtered.columns:
            le = LabelEncoder()
            data_filtered[column] = le.fit_transform(data_filtered[column].astype(str))

    # ディレクトリの作成
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # 処理済みデータをCSVファイルに保存
    data_filtered.to_csv(output_file_path, index=False)

    print(f"{boat_number}号艇のデータ前処理が完了しました")


# すべてのボートのデータを処理する
for i in range(1, 7):
    preprocess_boat_data(i)

print("すべてのボートのデータ前処理が完了しました")



