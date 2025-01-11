"""
@author: HAYASHI Yasuhito (dangom_ya)

CopyPolicy: 
    Released under the terms of the LGPLv2.1 or later.
"""
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse
import os

plt.rcParams.update({
    'lines.linewidth': 2,
    'grid.linestyle': '--',
    'axes.grid': True,
    'axes.facecolor': 'white',
    'axes.edgecolor': 'gray',
    'font.size': 11,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.figsize': (12, 8),
})

def downsample_events(data, sampling_ratio):
    return data.iloc[::sampling_ratio]

def plot_3d(file_path, output_file, sampling_ratio):
    data = pd.read_csv(file_path, header=None, names=['x', 'y', 'polarity', 'time'])
    data['time'] = data['time'] * 1e-3  # 時間をミリ秒に変換

    data = downsample_events(data, sampling_ratio)

    fig = plt.figure(figsize=(10, 8))
    ax3d = fig.add_subplot(111, projection='3d')

    colors = {1: 'black', 0: 'gray'}
    for polarity, group_data in data.groupby('polarity'):
        ax3d.scatter(
            group_data['time']/1000, group_data['x'], group_data['y'],
            s=1, c=colors[polarity], edgecolors='none', marker='.'
        )

    ax3d.set_xlabel('Time (s)')
    ax3d.set_ylabel('X')
    ax3d.set_zlabel('Y')

    ax3d.set_ylim([0, 1280])
    ax3d.set_zlim([720, 0])
    ax3d.view_init(elev=4, azim=-40)

    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a 3D scatter plot from CSV data with optional downsampling.")
    parser.add_argument('-i', '--input', default='./sampleData/recording_2024-12-10_11-30-57.csv', help="Path to the input CSV file")
    parser.add_argument('-o', '--output', default='./sampleData/plotAll.png', help="Path to save the output image")
    parser.add_argument('-r', '--sampling_ratio', type=int, default=10, help="Sampling ratio for downsampling events (default: 100)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The file '{args.input}' does not exist.")

    plot_3d(args.input, args.output, args.sampling_ratio)