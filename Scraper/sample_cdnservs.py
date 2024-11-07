import pandas as pd

file_path = 'final_websites_cdnservs.csv'
df = pd.read_csv(file_path)

random_seed = 42 
sampled_df = df.sample(n=500, random_state=random_seed)
output_file_path = 'sampled_cdn_servers.csv'
sampled_df.to_csv(output_file_path, index=False)

print(f"Randomly sampled 500 records saved to: {output_file_path}")
