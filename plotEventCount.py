import pandas as pd
import pickle
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

def plot_event_counts(pkl_file, output_file, time_bin_size=2):
    with open(pkl_file, 'rb') as f:
        df = pickle.load(f)

    print(f"Number of events: {len(df)}")

    if not pd.api.types.is_numeric_dtype(df['time']):
        df['time'] = pd.to_numeric(df['time'], errors='coerce')
        df = df.dropna(subset=['time'])  # NaN を削除

    df['time_bin'] = (df['time'] // time_bin_size) * time_bin_size

    event_counts = df.groupby('time_bin').size()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    ax.plot(event_counts.index / 1000, event_counts.values, label='Raw Event Count', color='red')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Event Count')
    ax.set_title('Event Count Over Time')

    ax.grid(True)
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved as {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot event counts over time from a .pkl file.")
    parser.add_argument('-i', '--input', default='./sampleData/recording_2024-12-10_11-30-57_filtered_results/filtered_events_all.pkl', help="Path to the input .pkl file")
    parser.add_argument('-b', '--bin_size', type=int, default=2, help="Time bin size in milliseconds (default: 2ms)")
    parser.add_argument('-o', '--output', default='./sampleData/plotEventCount.png', help="Path to save the output image")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise FileNotFoundError(f"The file '{args.input}' does not exist.")

    plot_event_counts(args.input, args.output, args.bin_size)