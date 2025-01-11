"""
@author: HAYASHI Yasuhito (dangom_ya)

CopyPolicy: 
    Released under the terms of the LGPLv2.1 or later.
"""
import pandas as pd
import matplotlib.pyplot as plt
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

def plot_event_counts(file_path, output_file, time_bin_size, sampling_ratio):
    data = pd.read_csv(file_path, header=None, names=['x', 'y', 'polarity', 'time'])
    data['time'] = data['time'] * 1e-3  # マイクロ秒をミリ秒に変換

    data = downsample_events(data, sampling_ratio)

    data['time_bin'] = (data['time'] // time_bin_size) * time_bin_size
    event_counts = data.groupby('time_bin').size()

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(event_counts.index / 1000, event_counts.values, label='Event Count', color='blue')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Event Count')
    ax.set_title('Event Count Over Time')

    ax.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot event counts over time from a CSV file with optional downsampling.")
    parser.add_argument('-i', '--input', default='./sampleData/recording_2024-12-10_11-30-57.csv', help="Path to the input CSV file")
    parser.add_argument('-b', '--bin_size', type=int, default=2, help="Time bin size in milliseconds (default: 2ms)")
    parser.add_argument('-o', '--output', default='./sampleData/plotEventCount.png', help="Path to save the output image")
    parser.add_argument('-r', '--sampling_ratio', type=int, default=10, help="Sampling ratio for downsampling events (default: 10)")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The file '{args.input}' does not exist.")

    plot_event_counts(args.input, args.output, args.bin_size, args.sampling_ratio)