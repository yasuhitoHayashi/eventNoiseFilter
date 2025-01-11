"""
@author: HAYASHI Yasuhito (dangom_ya)

CopyPolicy: 
    Released under the terms of the LGPLv2.1 or later.
"""
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import argparse
import os
import numpy as np

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

def plot_event_counts_with_sliding_window(pkl_file, output_file, time_bin_size, step_size):
    with open(pkl_file, 'rb') as f:
        df = pickle.load(f)

    print(f"Number of events: {len(df)}")

    if not pd.api.types.is_numeric_dtype(df['time']):
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        df = df.dropna(subset=['time'])  # NaN を削除

    max_time = df['time'].max()

    bins = np.arange(0, max_time, step_size)
    event_counts = [
        len(df[(df['time'] >= start) & (df['time'] < start + time_bin_size)])
        for start in bins
    ]

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    ax.plot(bins / 1000, event_counts, label='Sliding Window Event Count', color='blue')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Event Count')
    ax.set_title('Event Count Over Time')

    ax.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot event counts over time from a .pkl file with sliding window.")
    parser.add_argument('-i', '--input', default='./sampleData/recording_2024-12-10_11-30-57_filtered_results/filtered_events_all.pkl', help="Path to the input .pkl file")
    parser.add_argument('-b', '--bin_size', type=int, default=50, help="Time bin size in milliseconds (default: 50ms)")
    parser.add_argument('-s', '--step_size', type=int, default=10, help="Step size for the sliding window in milliseconds (default: 10ms)")
    parser.add_argument('-o', '--output', default='./sampleData/plotEventCount.png', help="Path to save the output image")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The file '{args.input}' does not exist.")

    plot_event_counts_with_sliding_window(args.input, args.output, args.bin_size, args.step_size)