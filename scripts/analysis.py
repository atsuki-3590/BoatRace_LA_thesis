import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib 
japanize_matplotlib.japanize()

# CSVファイルを読み込む (ファイル名を適宜変更してください)
file_path = 'data/raw/merged_data.csv'
data = pd.read_csv(file_path)

# 必要な列を確認
if '3連複_組番' not in data.columns or '3連複_払戻金' not in data.columns:
    raise ValueError("CSVファイルに '3連複_組番' または '3連複_払戻金' 列がありません。")

# データの型を確認し、必要に応じて型変換
# 例: 払戻金が文字列型の場合、数値型に変換
if data['3連複_払戻金'].dtype == 'object':
    data['3連複_払戻金'] = pd.to_numeric(data['3連複_払戻金'].str.replace(',', ''), errors='coerce')

# 組番ごとに頻度と平均払戻金を計算
result = data.groupby('3連複_組番')['3連複_払戻金'].agg(['count', 'mean']).reset_index()
result.columns = ['3連複_組番', '頻度', '平均払戻金']

# 全体に対する割合を計算
result['割合'] = (result['頻度'] / result['頻度'].sum()) * 100

# 割合の逆数を計算
result['割合の逆数'] = 100 / result['割合']

# 結果を頻度で降順ソート
result = result.sort_values(by='頻度', ascending=False)

# グラフを作成
plt.figure(figsize=(10, 6))

# 頻度の棒グラフ
plt.bar(result['3連複_組番'], result['頻度'], alpha=0.7, label='頻度')

# 平均払戻金の折れ線グラフ
plt.plot(result['3連複_組番'], result['平均払戻金'], color='red', marker='o', label='平均払戻金')

plt.xlabel('3連複_組番')
plt.ylabel('値')
plt.title('3連複 組番の頻度と平均払戻金')
plt.xticks(rotation=90)
plt.legend()
plt.tight_layout()
plt.show()

# 結果を表示
print(result)