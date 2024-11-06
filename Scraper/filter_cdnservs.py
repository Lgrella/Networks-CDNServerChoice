import pandas as pd
import os

# Paths for sample file, raw data folder, and output folder
sample_file_path = 'final_sampled_websites.csv'
raw_data_folder = 'raw_data'
output_folder = 'sampled_raw_data'

# Load the sample file
sample_df = pd.read_csv(sample_file_path)
sample_df.columns = ['id', 'website']  # Ensure the column name is 'website' for filtering

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate over all CSV files in the raw_data folder
for filename in os.listdir(raw_data_folder):
    if filename.endswith('.csv'):
        # Load each raw data file
        cdn_file_path = os.path.join(raw_data_folder, filename)
        cdn_df = pd.read_csv(cdn_file_path)
        
        # Standardize the column names for merging
        cdn_df.columns = ['website', 'ip_address', 'cdn_server']
        
        # Filter to keep only the records that match the sample websites
        filtered_cdn_df = cdn_df[cdn_df['website'].isin(sample_df['website'])]
        
        # Save the filtered data to a new CSV file in the output folder
        output_path = os.path.join(output_folder, f"{filename.split('.')[0]}_sampled.csv")
        filtered_cdn_df.to_csv(output_path, index=False)
        
        print(f"Filtered CDN records saved to: {output_path}")

