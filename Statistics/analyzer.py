import pandas as pd
import glob
import os
import numpy as np

# Use the current directory
directory = os.getcwd()

# Group files by `ny` prefix
grouped_files = {
    "sgp": glob.glob(f"{directory}/cdn_ping_stats_sgp_*.csv")
}

#read in csv
df = pd.read_csv(f"{directory}/cdn_ping_stats_sgp1.csv")

first_records = df.groupby("website").first().reset_index()
df_without_first = df.loc[df.index != df.groupby("website").head(1).index[0]]
min_median_rows = df_without_first.loc[df_without_first.groupby("website")["median"].idxmin()]  

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
merged_dataset.to_csv(f"{directory}/sgp1_compare.csv", index=False)

