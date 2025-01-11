import pandas as pd
import filter_events
import pickle
import os
from tqdm import tqdm
import argparse

def process_and_save(file_path):
    # 出力ディレクトリを設定（CSVファイル名をディレクトリ名に変換）
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join(os.path.dirname(file_path), f"{file_name}_filtered_results")
    os.makedirs(output_dir, exist_ok=True)

    # パラメータ設定
    N = 5   # 空間近傍範囲
    tau = 2  # 時間近傍範囲
    K_threshold = 2
    chunksize = 100000
    chunk_id = 0
    filtered_files = []

    # 総行数をカウント
    with open(file_path, 'r') as f:
        total_lines = sum(1 for _ in f)

    print("Start processing chunks...")

    # チャンクごとに処理
    for chunk in tqdm(pd.read_csv(file_path, header=None, names=['x', 'y', 'polarity', 'time'],
                                  dtype={'x': 'int32', 'y': 'int32', 'polarity': 'int8', 'time': 'int64'},
                                  chunksize=chunksize, engine='python'),
                      total=(total_lines // chunksize) + 1):
        # timeをusからmsへ変換
        chunk['time'] = chunk['time'] // 1000

        # polarity == 1のみ
        chunk = chunk[chunk['polarity'] == 1]
        if len(chunk) == 0:
            continue

        events = [filter_events.Event(row.x, row.y, row.time) for row in chunk.itertuples(index=False)]

        filtered = filter_events.filter_events(events, N, tau, K_threshold)

        filtered_list = [(e.x, e.y, e.time) for e in filtered]
        filtered_df = pd.DataFrame(filtered_list, columns=['x', 'y', 'time'])

        part_file = os.path.join(output_dir, f'filtered_events_part_{chunk_id}.pkl')
        with open(part_file, 'wb') as f:
            pickle.dump(filtered_df, f)
        filtered_files.append(part_file)

        chunk_id += 1

    print("All chunks processed. Now combining results...")

    all_filtered_dfs = []
    for f in sorted(filtered_files):
        with open(f, 'rb') as fh:
            df_part = pickle.load(fh)
            all_filtered_dfs.append(df_part)

    if len(all_filtered_dfs) > 0:
        combined_df = pd.concat(all_filtered_dfs, ignore_index=True)
    else:
        combined_df = pd.DataFrame(columns=['x', 'y', 'time'])

    final_output_file = os.path.join(output_dir, 'filtered_events_all.pkl')
    with open(final_output_file, 'wb') as f:
        pickle.dump(combined_df, f)

    print(f"Combined result saved to {final_output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a CSV file and filter events.")
    parser.add_argument('-i', '--input', default='./sampleData/recording_2024-12-10_14-07-33.csv', help="Path to the input CSV file")
    args = parser.parse_args()

    input_file = args.input
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file '{input_file}' does not exist.")

    process_and_save(input_file)