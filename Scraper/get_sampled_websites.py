import pandas as pd

# Load the CSV file
file_path = 'final_websites.csv'
websites_df = pd.read_csv(file_path)

# Rename the columns
websites_df.columns = ['id', 'website']

# Randomly select 100 rows with a fixed random seed for reproducibility
sampled_websites_df = websites_df.sample(n=100, random_state=42)

# Sort the sampled data by 'id' column in ascending order
sampled_websites_df = sampled_websites_df.sort_values(by='id').reset_index(drop=True)

# Save the sorted sampled data to a new CSV file
output_path = 'final_sampled_websites.csv'
sampled_websites_df.to_csv(output_path, index=False)

print("Random sample of 100 websites saved and sorted by id to:", output_path)
