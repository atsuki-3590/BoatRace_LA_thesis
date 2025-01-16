# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import japanize_matplotlib 
# japanize_matplotlib.japanize()

# # データの読み込み
# # file_path = 'betting_simulation/data/processed/test_predict_with_odds_20240611_20240731.csv'
# file_path = 'betting_simulation/data/processed/test_predict_with_odds_20240611_20240630.csv'
# df = pd.read_csv(file_path)

# # 逆数の積のデータフレームを作成
# inverse_product_df = pd.DataFrame({
#     'Combination': [
#         '1=2=3', '1=2=4', '1=2=5', '1=2=6', '1=3=4', '1=3=5', '1=3=6', '1=4=5', '1=4=6', '1=5=6',
#         '2=3=4', '2=3=5', '2=3=6', '2=4=5', '2=4=6', '2=5=6', '3=4=5', '3=4=6', '3=5=6', '4=5=6'
#     ],
#     # 'Inverse Product': [
#     #     3.285324, 2.802188, 3.402657, 3.664400, 3.092069, 3.754656, 4.043475, 3.202501, 3.448847, 4.187885,
#     #     3.961714, 4.810653, 5.180703, 4.103204, 4.418835, 5.365728, 4.527673, 4.875956, 5.920803, 5.050097
#     # ]
#     'Inverse Product': [0.0] * 20 
#     # 'Inverse Product': [5.0] * 20 
#     # 'Inverse Product': [6.0] * 20 
#     # 'Inverse Product': [7.0] * 20 
#     # 'Inverse Product': [8.0] * 20 
#     # 'Inverse Product': [9.0] * 20 
#     # 'Inverse Product': [10.0] * 20 
#     # 'Inverse Product': [15.0] * 20 
#     # 'Inverse Product': [20.0] * 20
#     # 'Inverse Product': [22.0] * 20 
#     # 'Inverse Product': [25.0] * 20
#     # 'Inverse Product': [26.0] * 20
#     # 'Inverse Product': [27.0] * 20
#     # 'Inverse Product': [30.0] * 20
# })

# # 1. `predict_result_1`から`predict_result_6`の列の中で「1」の数が2つより多い行をフィルタリング
# filtered_df = df[df[['predict_result_1', 'predict_result_2', 'predict_result_3', 'predict_result_4', 'predict_result_5', 'predict_result_6']].sum(axis=1) > 2]

# # 的中と最大オッズの追跡
# max_odds = 0
# race_code_of_max_odds = None
# match_count = 0
# total_purchases_count = 0 

# # 2. フィルタリングされた行から「1」が現れる列の組み合わせを抽出
# relevant_combinations = []
# for index, row in filtered_df.iterrows():
#     selected_columns = [f"{i+1}" for i in range(6) if row[f"predict_result_{i+1}"] == 1]
#     combinations = []
#     for i in range(len(selected_columns)):
#         for j in range(i+1, len(selected_columns)):
#             for k in range(j+1, len(selected_columns)):
#                 combinations.append(f"{selected_columns[i]}={selected_columns[j]}={selected_columns[k]}")
#     relevant_combinations.append(combinations)

# # 3. 修正された購入と払い戻しの計算
# total_purchases = 0
# total_payouts = 0
# bet_amount = 100  # 賭け金額を設定（例として100円）

# winning_odds = []
# purchased_odds = []

# for i, combinations in enumerate(relevant_combinations):
#     row = filtered_df.iloc[i]
#     for combination in combinations:
#         inverse_value = inverse_product_df[inverse_product_df['Combination'] == combination]['Inverse Product'].values[0]
#         # 逆数の積よりもオッズが大きい場合に購入
#         if row[combination] > inverse_value:
#             total_purchases += bet_amount  # 100円ずつ購入すると仮定
#             total_purchases_count += 1  # 購入件数を増加
#             purchased_odds.append(row[combination])  # 購入オッズを記録
#             # この組み合わせが実際の結果と一致するか確認
#             if combination == row['result']:
#                 total_payouts += bet_amount * row[combination]  # 実際の払い戻しは賭け金 × オッズ
#                 winning_odds.append(row[combination])
#                 match_count += 1 # 的中回数をカウント
#                 odds = row[combination] 
#                 if odds > max_odds:
#                     max_odds = odds
#                     race_code_of_max_odds = row['レースコード'] 

# hit_rate = round(match_count / total_purchases_count * 100, 2) if total_purchases_count > 0 else 0.0

# # 結果の表示
# total_purchases = int(total_purchases)
# total_payouts = int(total_payouts)
# collection_rate = round(total_payouts / total_purchases * 100, 2)

# print(f"購入金額 : {total_purchases}円")
# print(f"払戻金額 : {total_payouts}円")
# print(f"回収率 : {collection_rate}%")
# print(f"的中件数 : {match_count}件")
# print(f"的中率 : {hit_rate}%")

# print(f"最大オッズのレースコード: {race_code_of_max_odds}, 最大オッズ: {max_odds}")


# # ビンの幅を5に設定
# bin_width = 2.5
# bins = np.arange(0, max(max(winning_odds), max(purchased_odds)) + bin_width, bin_width)

# # 的中オッズと購入オッズのヒストグラムを重ねて描画
# plt.figure(figsize=(10, 6))

# # 的中オッズのヒストグラム
# plt.hist(winning_odds, bins=bins, color='blue', edgecolor='black', alpha=0.5, label='的中オッズ')

# # 購入オッズのヒストグラム
# plt.hist(purchased_odds, bins=bins, color='green', edgecolor='black', alpha=0.5, label='購入オッズ')

# plt.title('的中オッズと購入オッズの分布')
# plt.xlabel('オッズ')
# plt.ylabel('頻度')
# plt.legend(loc='upper right')
# plt.grid(True)
# plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib 
japanize_matplotlib.japanize()

# データの読み込み
file_path = 'betting_simulation/data/processed/test_predict_with_odds_20240611_20240630.csv'
df = pd.read_csv(file_path)

# 逆数の積のデータフレームを作成
inverse_product_df = pd.DataFrame({
    'Combination': [
        '1=2=3', '1=2=4', '1=2=5', '1=2=6', '1=3=4', '1=3=5', '1=3=6', '1=4=5', '1=4=6', '1=5=6',
        '2=3=4', '2=3=5', '2=3=6', '2=4=5', '2=4=6', '2=5=6', '3=4=5', '3=4=6', '3=5=6', '4=5=6'
    ],
    'Inverse Product': [0.0] * 20 
})

# 購入条件を定義する関数（最低購入オッズを追加）
def purchase_condition(combination, include_boat=None, exclude_boat=None, odds=None, min_odds=None):
    """
    購入条件を判定する関数。
    - include_boat: 必ず購入する艇番号を指定 (例: ['6'])
    - exclude_boat: 購入を除外する艇番号を指定 (例: ['1'])
    - odds: 該当組み合わせのオッズ
    - min_odds: 最低購入オッズを指定 (例: 3.0)
    """
    if include_boat and any(boat in combination for boat in include_boat):
        return True  # 必ず購入
    if exclude_boat and any(boat in combination for boat in exclude_boat):
        return False  # 購入しない
    if min_odds and odds is not None and odds < min_odds:
        return False  # 最低オッズ未満なら購入しない
    return True  # 上記条件を満たさない場合は購入する

# 柔軟な条件を設定
include_boat = []  # 必ず購入する艇番号 (例: ['6'])
exclude_boat = []  # 購入を除外する艇番号 (例: ['1'])
min_odds = 10.0     # 最低購入オッズを設定（例: 3.0）

# 1. `predict_result_1`から`predict_result_6`の列の中で「1」の数が2つより多い行をフィルタリング
filtered_df = df[df[['predict_result_1', 'predict_result_2', 'predict_result_3', 'predict_result_4', 'predict_result_5', 'predict_result_6']].sum(axis=1) > 2]

# 2. フィルタリングされた行から「1」が現れる列の組み合わせを抽出
relevant_combinations = []
for index, row in filtered_df.iterrows():
    selected_columns = [f"{i+1}" for i in range(6) if row[f"predict_result_{i+1}"] == 1]
    combinations = []
    for i in range(len(selected_columns)):
        for j in range(i+1, len(selected_columns)):
            for k in range(j+1, len(selected_columns)):
                combination = f"{selected_columns[i]}={selected_columns[j]}={selected_columns[k]}"
                # 購入条件を満たすか判定
                odds = row[combination] if combination in row else None
                if purchase_condition(combination, include_boat, exclude_boat, odds, min_odds):
                    combinations.append(combination)
    relevant_combinations.append(combinations)

# 3. 修正された購入と払い戻しの計算
total_purchases = 0
total_payouts = 0
bet_amount = 100  # 賭け金額を設定（例として100円）

winning_odds = []
purchased_odds = []

max_odds = 0
race_code_of_max_odds = None
match_count = 0
total_purchases_count = 0

for i, combinations in enumerate(relevant_combinations):
    row = filtered_df.iloc[i]
    for combination in combinations:
        inverse_value = inverse_product_df[inverse_product_df['Combination'] == combination]['Inverse Product'].values[0]
        # 逆数の積よりもオッズが大きい場合に購入
        if row[combination] > inverse_value:
            total_purchases += bet_amount  # 100円ずつ購入すると仮定
            total_purchases_count += 1  # 購入件数を増加
            purchased_odds.append(row[combination])  # 購入オッズを記録
            # この組み合わせが実際の結果と一致するか確認
            if combination == row['result']:
                total_payouts += bet_amount * row[combination]  # 実際の払い戻しは賭け金 × オッズ
                winning_odds.append(row[combination])
                match_count += 1  # 的中回数をカウント
                odds = row[combination]
                if odds > max_odds:
                    max_odds = odds
                    race_code_of_max_odds = row['レースコード']

hit_rate = round(match_count / total_purchases_count * 100, 2) if total_purchases_count > 0 else 0.0

# 結果の表示
total_purchases = int(total_purchases)
total_payouts = int(total_payouts)
collection_rate = round(total_payouts / total_purchases * 100, 2)

print(f"購入金額 : {total_purchases}円")
print(f"払戻金額 : {total_payouts}円")
print(f"回収率 : {collection_rate}%")
print(f"的中件数 : {match_count}件")
print(f"的中率 : {hit_rate}%")

print(f"最大オッズのレースコード: {race_code_of_max_odds}, 最大オッズ: {max_odds}")

# ビンの幅を5に設定
bin_width = 2.5
bins = np.arange(0, max(max(winning_odds), max(purchased_odds)) + bin_width, bin_width)

# 的中オッズと購入オッズのヒストグラムを重ねて描画
plt.figure(figsize=(10, 6))

# 的中オッズのヒストグラム
plt.hist(winning_odds, bins=bins, color='blue', edgecolor='black', alpha=0.5, label='的中オッズ')

# 購入オッズのヒストグラム
plt.hist(purchased_odds, bins=bins, color='green', edgecolor='black', alpha=0.5, label='購入オッズ')

plt.title('的中オッズと購入オッズの分布')
plt.xlabel('オッズ')
plt.ylabel('頻度')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()
