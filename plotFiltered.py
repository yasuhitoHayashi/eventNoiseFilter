import pandas as pd
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 明示的にインポート

# 保存されたファイル名（パス）を指定
pkl_file = '/Volumes/yhData/expData/241210_hirosaki/filtered_results/filtered_events_all.pkl'

# pklファイル読み込み
with open(pkl_file, 'rb') as f:
    df = pickle.load(f)

print(len(df))
# DataFrameのカラムが['x', 'y', 'time']
x = df['x'].values
y = df['y'].values
t = df['time'].values

# 3Dプロットのセットアップ
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# 散布図プロット: x軸、y軸、z軸にそれぞれ x, y, time を割り当て
sc = ax.scatter(x, y, t, c=t, cmap='viridis', s=1, alpha=1)

# 軸ラベル設定
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_ylim(720,0)
ax.set_xlim(0,1280)
ax.set_zlabel('Time (ms)')

plt.show()