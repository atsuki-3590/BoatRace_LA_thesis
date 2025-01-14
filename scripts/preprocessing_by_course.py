# コースごとにデータ前処理
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# ファイルパスを変数に格納
raw_file_path = 'data/raw/merged_data.csv'
processed_dir = 'data/processed/'

os.makedirs(processed_dir, exist_ok=True)

modified_file_path = f"{processed_dir}data_by_course.csv"

df = pd.read_csv(raw_file_path, low_memory=False)

# 削除する列を指定
columns_to_drop = [
    '1枠_艇番', '2枠_艇番', '3枠_艇番', '4枠_艇番', '5枠_艇番', '6枠_艇番',
    '1枠_登録番号', '2枠_登録番号', '3枠_登録番号', '4枠_登録番号', '5枠_登録番号', '6枠_登録番号',
    '1枠_年齢', '2枠_年齢', '3枠_年齢', '4枠_年齢', '5枠_年齢', '6枠_年齢',
    '1枠_モーター番号', '2枠_モーター番号', '3枠_モーター番号', '4枠_モーター番号', '5枠_モーター番号', '6枠_モーター番号',
    '1枠_ボート番号', '2枠_ボート番号', '3枠_ボート番号', '4枠_ボート番号', '5枠_ボート番号', '6枠_ボート番号',
    '1枠_選手名', '2枠_選手名', '3枠_選手名', '4枠_選手名', '5枠_選手名', '6枠_選手名',
    '1枠_支部', '2枠_支部', '3枠_支部', '4枠_支部', '5枠_支部', '6枠_支部',
    '1着_登録番号', '2着_登録番号', '3着_登録番号', '4着_登録番号', '5着_登録番号', '6着_登録番号',
    '1着_着順', '2着_着順', '3着_着順', '4着_着順', '5着_着順', '6着_着順', 
    '1着_選手名', '2着_選手名', '3着_選手名', '4着_選手名', '5着_選手名', '6着_選手名',
    '1着_進入コース', '2着_進入コース', '3着_進入コース', '4着_進入コース', '5着_進入コース', '6着_進入コース', 
    '日次', 'レース日', '距離', '決まり手'
]

# 指定した列を削除
new_data = df.drop(columns=columns_to_drop)

print(new_data.columns)

print("データ前処理を開始します")

# 新しいカラムを追加
# new_data['1号艇勝敗'] = new_data['1着_艇番'].apply(lambda x: 1 if x == 1 else 0)

race_course_to_stand_distance = {
    "桐生": 47,
    "戸田": 37,
    "江戸川": 37.1,
    "平和島": 37,
    "多摩川": 41,

    "浜名湖": 42.7,
    "蒲郡": 41.3,
    "常滑": 40,
    "津": 40,

    "三国": 45,
    "びわこ": 47,
    "住之江": 45,
    "尼崎": 49.1,

    "鳴門": 45,
    "丸亀": 42,

    "児島": 43,
    "宮島": 40,
    "徳山": 45,
    "下関": 43,

    "若松": 41,
    "芦屋": 50,
    "福岡": 50,
    "唐津": 42,
    "大村": 48
}

# 基本となる八方位の風向リスト（順番は固定）
wind_directions = ['追い風', '左追い風', '左横風', '左向かい風', '向かい風', '右向かい風', '右横風', '右追い風']
directions = ['北', '北東', '東', '南東', '南', '南西', '西', '北西']

# 各レース場における風向の開始位置を定義
starting_wind_direction = {
    "桐生": "北",  # 追い風が北に対応
    "戸田": "西",  
    "江戸川": "南",
    "平和島": "南",
    "多摩川": "東",

    "浜名湖": "北",
    "蒲郡": "北東",
    "常滑": "東",
    "津": "東",

    "三国": "北",
    "びわこ": "北",
    "住之江": "北",
    "尼崎": "北東",

    "鳴門": "北西",
    "丸亀": "南",

    "児島": "北",
    "宮島": "北東",
    "徳山": "南東",
    "下関": "北東",

    "若松": "北東",
    "芦屋": "西",
    "福岡": "西",
    "唐津": "北",
    "大村": "南西",
}

# 風向の変換関数を定義
def transform_wind_direction(row):
    race_course = row['レース場']
    wind_dir = row['風向']
    
    # 風向が無風の場合、そのまま返す
    if wind_dir == '無風':
        return wind_dir
    
    # レース場ごとの風向の開始位置を特定
    if race_course in starting_wind_direction:
        start_dir = starting_wind_direction[race_course]
        # 開始位置に合わせてリストを回転させる
        index = directions.index(start_dir)
        rotated_wind_directions = wind_directions[index:] + wind_directions[:index]
        # 風向を変換
        return rotated_wind_directions[directions.index(wind_dir)]
    else:
        return wind_dir
    


def transform_data(df):
    # 展示タイムのカラムを特定し、数値型に変換
    exhibition_time_columns = [col for col in df.columns if '展示タイム' in col]
    for col in exhibition_time_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # 'K .' を含む行を検出
    mask = (df == 'K .').any(axis=1)
    invalid_time_count = mask.sum()  # 'K .' を含む行の数をカウント
    df = df[~mask]  # 'K .' を含む行を削除
    
    # NaNが含まれる行を削除する前のデータの行数
    original_count = df.shape[0]
    
    # NaNが含まれる行を削除
    df.dropna(inplace=True)

    # NaNを含む行を削除した後の行数の差を計算
    deleted_count = original_count - df.shape[0]
    
    # 'K .' を含む行数とNaNが含まれる行数を合計した削除行数を報告
    total_deleted = deleted_count + invalid_time_count
    print(f"合計 {total_deleted} 行が削除されました。")

    df['スタンド距離'] = df['レース場'].map(race_course_to_stand_distance)

    # 風向を変換
    df['風向'] = df.apply(transform_wind_direction, axis=1)

    # 変換したデータを格納するリスト
    transformed_rows = []
    
    # 1行ずつループ
    for _, row in df.iterrows():
        for i in range(1, 7):
            # 枠別データ抽出
            frame_data = {
                '枠': i,
                '体重': row[f'{i}枠_体重'],
                '級別': row[f'{i}枠_級別'],
                '全国勝率': row[f'{i}枠_全国勝率'],
                '全国2連対率': row[f'{i}枠_全国2連対率'],
                '当地勝率': row[f'{i}枠_当地勝率'],
                '当地2連対率': row[f'{i}枠_当地2連対率'],
                'モーター2連対率': row[f'{i}枠_モーター2連対率'],
                'ボート2連対率': row[f'{i}枠_ボート2連対率']
            }
            # 共通データ抽出
            frame_data.update({
                'レースコード': row['レースコード'],
                'レース場': row['レース場'],
                'レース回': row['レース回'],
                '天気': row['天気'],
                '風向': row['風向'],
                '風速': row['風速'],
                '波の高さ': row['波の高さ'],
                'スタンド距離': row['スタンド距離'],
                # '距離': row['距離'],
                # '決まり手': row['決まり手'],
            })
            # one-hot-encodingで順位と結果を設定
            for j in range(1, 7):
                if row[f'{j}着_艇番'] == i:
                    frame_data['順位'] = int(j)
                    frame_data['結果'] = int(1 if j == 1 else 0)
                    frame_data['3連複_結果'] = int(1 if j >= 1 and 3 >= j else 0)
                    frame_data['展示タイム'] = row[f'{j}着_展示タイム']
                    break

            transformed_rows.append(frame_data)

    transformed_df = pd.DataFrame(transformed_rows)
    # columns_order = ['レースコード', 'レース場', 'レース回', '天気', '風向', '風速', '波の高さ', 'スタンド距離', '距離', '決まり手', '枠', '体重', '級別', '全国勝率', '全国2連対率', '当地勝率', '当地2連対率', 'モーター2連対率', 'ボート2連対率', '順位', '結果']
    columns_order = ['レースコード', 'レース場', 'レース回', '天気', '風向', '風速', '波の高さ', 'スタンド距離', '枠', '体重', '級別', '全国勝率', '全国2連対率', '当地勝率', '当地2連対率', 'モーター2連対率', 'ボート2連対率', '展示タイム', '順位', '結果', '3連複_結果']
    transformed_df = transformed_df[columns_order]

    return transformed_df

transformed_df = transform_data(new_data)

print("コースごとのデータを作成しました")

# 数値型に変換する対象カラムを指定
columns_to_check = ['全国勝率', '全国2連対率', '当地勝率', '当地2連対率', 'モーター2連対率', 'ボート2連対率', '展示タイム']

# 各カラムについて非数値データを探索
for column in columns_to_check:
    # 文字列を数値に変換し、変換できない場合はNaNに置き換える
    temp_df = transformed_df[column].apply(pd.to_numeric, errors='coerce')
    
    # NaNが発生したデータ（元が非数値文字列）をフィルタリング
    non_numeric_data = transformed_df[temp_df.isna()][column]
    
    # 非数値データがあればその一部を表示
    if not non_numeric_data.empty:
        print(f"カラム '{column}' に含まれる非数値データの一部:")
        print(non_numeric_data.unique()[:10])  # 最初の10個のユニークな非数値エントリを表示
    else:
        print(f"カラム '{column}' には非数値データは含まれていません。")



# Zスコアカラムを追加
def add_z_score(df, column):
    mean = df.groupby('レースコード')[column].transform('mean')
    std = df.groupby('レースコード')[column].transform('std')
    df[f'{column}_Zスコア'] = (df[column] - mean) / std

columns_to_add_z = ['全国勝率', '全国2連対率', '当地勝率', '当地2連対率', 'モーター2連対率', 'ボート2連対率', '展示タイム']
for column in columns_to_add_z:
    add_z_score(transformed_df, column)



os.makedirs(processed_dir, exist_ok=True)
transformed_df.to_csv(modified_file_path, index=False)

print("データ前処理が完了しました")



# # 1号艇のデータのみ抽出
# boat1_df = transformed_df[transformed_df['枠'] == 1]
# boat1_file_path = f"{processed_dir}data_boat1.csv"

# # CSVファイルとして保存
# transformed_df.to_csv(modified_file_path, index=False)
# boat1_df.to_csv(boat1_file_path, index=False)

# print("1号艇のデータを作成しました")


for i in range(1, 7):
    boat1_df = transformed_df[transformed_df['枠'] == i]
    boat1_file_path = f"{processed_dir}data_boat{i}.csv"

    # CSVファイルとして保存
    transformed_df.to_csv(modified_file_path, index=False)
    boat1_df.to_csv(boat1_file_path, index=False)

    print(f"{i}号艇のデータを作成しました")