import pandas as pd
import filter_events
import pickle
import os
from tqdm import tqdm
import glob
import argparse
from multiprocessing import Pool, cpu_count

# コマンドライン引数を設定
parser = argparse.ArgumentParser(description="Process a CSV file and filter events.")
parser.add_argument('-i', '--input', required=True, help="Path to the input CSV file")
args = parser.parse_args()

# 入力ファイルパスを取得
file_path = args.input
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist.")

# 出力ディレクトリを設定（CSVファイル名をディレクトリ名に変換）
file_name = os.path.splitext(os.path.basename(file_path))[0]  # CSVファイル名（拡張子なし）
output_dir = os.path.join(os.path.dirname(file_path), file_name)
os.makedirs(output_dir, exist_ok=True)

# パラメータ設定
N = 5   # 空間近傍範囲
tau = 2  # 時間近傍範囲
K_threshold = 2

chunksize = 100000

def process_chunk(chunk_data):
    """1つのチャンクを処理する関数"""
    chunk_id, chunk = chunk_data
    
    # timeをusからmsへ変換
    chunk['time'] = chunk['time'] // 1000

    # polarity == 1のみ抽出
    chunk = chunk[chunk['polarity'] == 1]
    if len(chunk) == 0:
        return None, None

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

    return chunk_id, part_file

# 総行数をカウント
with open(file_path, 'r') as f:
    total_lines = sum(1 for _ in f)

chunk_data_generator = (
    (i, chunk) for i, chunk in enumerate(
        pd.read_csv(file_path, header=None, names=['x', 'y', 'polarity', 'time'],
                    dtype={'x': 'int32', 'y': 'int32', 'polarity': 'int8', 'time': 'int64'},
                    chunksize=chunksize, engine='python')
    )
)

# 並列処理
print("Start processing chunks...")
with Pool(cpu_count()) as pool:
    results = list(tqdm(pool.imap(process_chunk, chunk_data_generator), total=(total_lines // chunksize) + 1))

# 有効な結果をフィルタリング
filtered_files = [result[1] for result in results if result[1] is not None]

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
