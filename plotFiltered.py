import pandas as pd
import pickle
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

def plot_from_pkl(pkl_file, output_file):
    with open(pkl_file, 'rb') as f:
        df = pickle.load(f)

    print(f"Number of events: {len(df)}")

    t = df['time'].values
    x = df['x'].values
    y = df['y'].values

    fig = plt.figure(figsize=(10, 8))
    ax3d = fig.add_subplot(111, projection='3d')

    sc = ax3d.scatter(t/1000, x, y, cmap='viridis', s=1, alpha=1)

    ax3d.set_xlabel('Time (s)')
    ax3d.set_ylabel('X')
    ax3d.set_zlabel('Y')
    ax3d.set_ylim(0, 1280)
    ax3d.set_zlim(720, 0)
    ax3d.view_init(elev=4, azim=-40)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="3D scatter plot from a .pkl file.")
    parser.add_argument('-i', '--input',default='./sampleData/recording_2024-12-10_11-30-57_filtered_results/filtered_events_all.pkl', help="Path to the input .pkl file")
    parser.add_argument('-o', '--output', default='./sampleData/plotFiltered.png', help="Path to save the output image")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The file '{args.input}' does not exist.")

    plot_from_pkl(args.input,args.output)