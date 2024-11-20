import pandas as pd
import glob
import os
import numpy as np

# Use the current directory
directory = os.getcwd()

# Group files by `ny` prefix
grouped_files = {
    "ny1": glob.glob(f"{directory}/cdn_ping_stats_ny1_*.csv"),
    "ny2": glob.glob(f"{directory}/cdn_ping_stats_ny2_*.csv"),
    "ny3": glob.glob(f"{directory}/cdn_ping_stats_ny3_*.csv"),
}

results = {}

for ny, file_list in grouped_files.items():
    all_data = []  # To store data across all CSVs for this group
    
    for file in file_list:
        df = pd.read_csv(file)
        all_data.append(df[['min', 'max', 'mean', 'median']])  # Select relevant columns
    
    combined_df = pd.concat(all_data, ignore_index=True)
    global_min = combined_df['min'].min()
    global_max = combined_df['max'].max()
    global_mean = combined_df['mean'].mean()
    global_median = np.median(combined_df['median'])
    
    results[ny] = {
        "global_min": global_min,
        "global_max": global_max,
        "global_mean": global_mean,
        "global_median": global_median,
    }

for ny, stats in results.items():
    print(f"Global stats for {ny}:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

