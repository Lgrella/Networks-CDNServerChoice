import pandas as pd
import glob
import os
import numpy as np
import matplotlib.pyplot as plt

# Use the current directory
directory = os.getcwd()

# Group files by prefix to combine batches
file_patterns = ["cdn_ping_stats_ams*.csv", "cdn_ping_stats_blr*.csv","cdn_ping_stats_tor*.csv",
                "cdn_ping_stats_fra*.csv", "cdn_ping_stats_lon*.csv", "cdn_ping_stats_sgp*.csv",
                 "cdn_ping_stats_syd*.csv", "cdn_ping_stats_ny1*.csv", "cdn_ping_stats_ny2*.csv",
                 "cdn_ping_stats_ny3*.csv", "cdn_ping_stats_sfo02*.csv", "cdn_ping_stats_sfo03*.csv"]
combined_dataframes = {}

# Loop through each pattern
for pattern in file_patterns:
    files = glob.glob(pattern)
    combined_df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    combined_dataframes[pattern.split('_')[3].split('*')[0]] = combined_df

# Example: Access combined DataFrame for 'ams' files
#ams_combined = combined_dataframes["ams"]

# blr_combined = combined_dataframes["blr"]
# fra_combined = combined_dataframes["fra"]

# lon_combined = combined_dataframes["lon"]
# sgp_combined = combined_dataframes["sgp"]
# syd_combined = combined_dataframes["syd"]

# tor_combined = combined_dataframes["tor"]
# ny1_combined = combined_dataframes["ny1"]
# ny2_combined = combined_dataframes["ny2"]

# ny3_combined = combined_dataframes["ny3"]
# sfo02_combined = combined_dataframes["sfo02"]
# sfo03_combined = combined_dataframes["sfo03"]

#loop through each combined dataframe
for key, value in combined_dataframes.items():
    df = value
    first_records = df.groupby("website").first().reset_index()
    min_median_rows = df.loc[df.groupby("website")["median"].idxmin()]  

    merged_dataset = pd.merge(
        first_records, 
        min_median_rows[["website", "cdn", "median"]], 
        on="website", 
        suffixes=("_first", "_min_median")
    )

    merged_dataset["diff"] = merged_dataset["median_first"] - merged_dataset["median_min_median"]

    #create a flag if cdn_min_median is the same as cdn_first
    merged_dataset["CDNChoiceGood"] = merged_dataset["cdn_first"] == merged_dataset["cdn_min_median"]

    # Filter for bad choices
    bad_choices = merged_dataset[merged_dataset['CDNChoiceGood'] == False]

    # Histogram of 'diff' values
    plt.hist(bad_choices['diff'], bins=40, color='blue', alpha=0.7)
    plt.title("Distribution of how much time is given up by choosing the wrong CDN\n" + key)
    plt.xlabel("Time (ms)")
    plt.ylabel("Frequency")
    plt.savefig(f"{directory}/Combined/viz/{key}_histogram.png")
    plt.close()

    #get summary statistics of CDNChoiceGood for each file and diff where CDNChoiceGood is False:
    #create a table with the summary statistics for excel with each row being a different file
    summary_table = pd.DataFrame()
    summary_table["File"] = [key]
    summary_table["Total"] = [len(merged_dataset)]
    summary_table["Good Choices"] = [len(merged_dataset[merged_dataset["CDNChoiceGood"]])]
    summary_table["Bad Choices"] = [len(merged_dataset[merged_dataset["CDNChoiceGood"] == False])]
    summary_table["Good Choice %"] = [len(merged_dataset[merged_dataset["CDNChoiceGood"]]) / len(merged_dataset)]
    summary_table["Bad Choice %"] = [len(merged_dataset[merged_dataset["CDNChoiceGood"] == False]) / len(merged_dataset)]
    summary_table["Median Diff"] = [np.median(merged_dataset.loc[merged_dataset["CDNChoiceGood"] == False, "diff"].astype(float))]
    summary_table["Mean Diff"] = [np.mean(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"])]
    summary_table["Max Diff"] = [np.max(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"])]
    summary_table["Min Diff"] = [np.min(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"])]
    summary_table["Std Dev Diff"] = [np.std(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"])]
    summary_table["25th Percentile Diff"] = [np.percentile(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"], 25)]
    summary_table["75th Percentile Diff"] = [np.percentile(merged_dataset[merged_dataset["CDNChoiceGood"] == False]["diff"], 75)]
    
    if 'all_summary_tables' not in locals():
        all_summary_tables = summary_table
    else:
        all_summary_tables = pd.concat([all_summary_tables, summary_table], ignore_index=True)

all_summary_tables.to_csv(f"{directory}/Combined/summary_table.csv", index=False)
"""
#read in csv
df = pd.read_csv(f"{directory}/cdn_ping_stats_lon4.csv")

first_records = df.groupby("website").first().reset_index()
min_median_rows = df.loc[df.groupby("website")["median"].idxmin()]  

merged_dataset = pd.merge(
    first_records, 
    min_median_rows[["website", "cdn", "median"]], 
    on="website", 
    suffixes=("_first", "_min_median")
)

merged_dataset["diff"] = merged_dataset["median_first"] - merged_dataset["median_min_median"]

#create a flag if cdn_min_median is the same as cdn_first
merged_dataset["CDNChoiceGood"] = merged_dataset["cdn_first"] == merged_dataset["cdn_min_median"]

print(merged_dataset)

#write to csv
merged_dataset.to_csv(f"{directory}/lon4_compare.csv", index=False)

"""