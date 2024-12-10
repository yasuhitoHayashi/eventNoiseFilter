import pandas as pd
import filter_events
import pickle
import os
from tqdm import tqdm
import glob
import argparse

# コマンドライン引数を設定
parser = argparse.ArgumentParser(description="Process a CSV file and filter events.")
parser.add_argument('-i', '--input', required=True, help="Path to the input CSV file")
args = parser.parse_args()

# 入力ファイルパスを取得
file_path = args.input
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist.")

# 出力ディレクトリを設定（入力ファイルと同じディレクトリ内に作成）
output_dir = os.path.join(os.path.dirname(file_path), "filtered_results")
os.makedirs(output_dir, exist_ok=True)

# パラメータ設定
N = 5   # 空間近傍範囲
tau = 2  # 時間近傍範囲
K_threshold = 2

# 総行数をカウント（ヘッダーがある・ないに応じて調整）
with open(file_path, 'r') as f:
    total_lines = sum(1 for _ in f)

chunksize = 100000
chunk_id = 0
filtered_files = []

print("Start processing chunks...")

for chunk in tqdm(pd.read_csv(file_path, header=None, names=['x', 'y', 'polarity', 'time'],
                              dtype={'x': 'int32', 'y': 'int32', 'polarity': 'int8', 'time': 'int64'},
                              chunksize=chunksize, engine='python'),
                  total=(total_lines // chunksize) + 1):
    # timeをusからmsへ変換
    chunk['time'] = chunk['time'] // 1000

    # polarity == 1のみ抽出
    chunk = chunk[chunk['polarity'] == 1]
    if len(chunk) == 0:
        # このチャンクには有効なイベントがない
        continue

    # Eventオブジェクトリスト作成
    events = [filter_events.Event(row.x, row.y, row.time) for row in chunk.itertuples(index=False)]

    # チャンク単位でフィルタリング
    filtered = filter_events.filter_events(events, N, tau, K_threshold)

    # データフレーム化
    filtered_list = [(e.x, e.y, e.time) for e in filtered]
    filtered_df = pd.DataFrame(filtered_list, columns=['x', 'y', 'time'])

    # 部分結果をファイル保存
    part_file = os.path.join(output_dir, f'filtered_events_part_{chunk_id}.pkl')
    with open(part_file, 'wb') as f:
        pickle.dump(filtered_df, f)
    filtered_files.append(part_file)

    chunk_id += 1

print("All chunks processed. Now combining results...")

# 全ての部分ファイルを結合
all_filtered_dfs = []
for f in sorted(filtered_files):
    with open(f, 'rb') as fh:
        df_part = pickle.load(fh)
        all_filtered_dfs.append(df_part)

if len(all_filtered_dfs) > 0:
    combined_df = pd.concat(all_filtered_dfs, ignore_index=True)
else:
    combined_df = pd.DataFrame(columns=['x', 'y', 'time'])

# 最終ファイル保存
final_output_file = os.path.join(output_dir, 'filtered_events_all.pkl')
with open(final_output_file, 'wb') as f:
    pickle.dump(combined_df, f)

print(f"Combined result saved to {final_output_file}")