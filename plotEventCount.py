import pandas as pd
import pickle
import matplotlib.pyplot as plt
import numpy as np

pkl_file = '/Volumes/yhData/expData/241210_hirosaki/filtered_results/filtered_events_all.pkl'

with open(pkl_file, 'rb') as f:
    df = pickle.load(f)

print(len(df))

time_bin_size = 2  # 2ms間隔
df['time_bin'] = (df['time'] // time_bin_size) * time_bin_size

event_counts = df.groupby('time_bin').size()


fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(event_counts.index/1000, event_counts.values, label='Raw Event Count', color='red')

ax.set_xlabel('Time (s)', fontsize=12)
ax.set_ylabel('Event Count', fontsize=12)
ax.set_title('Event Count Over Time', fontsize=14)

ax.grid(True)
ax.legend()

plt.show()