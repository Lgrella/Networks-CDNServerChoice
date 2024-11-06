import pandas as pd
import os

# Directory containing the processed sampled files
input_folder = 'sampled_raw_data'
output_file = 'aggregated_cdn_servers.csv'

# Dictionary to store website and associated CDN servers
cdn_servers_dict = {}

# Iterate over all CSV files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)
        
        # Group CDN servers by website
        for index, row in df.iterrows():
            website = row['website']
            cdn_server = row['cdn_server']
            
            # Add cdn_server to the list for the website
            if website not in cdn_servers_dict:
                cdn_servers_dict[website] = set()
            cdn_servers_dict[website].add(cdn_server)

# Convert the dictionary to a DataFrame
aggregated_data = {'website': [], 'cdn_servers': []}
for website, cdn_servers in cdn_servers_dict.items():
    aggregated_data['website'].append(website)
    # Join all CDN servers for each website into a single string, separated by semicolons
    aggregated_data['cdn_servers'].append('; '.join(cdn_servers))

aggregated_df = pd.DataFrame(aggregated_data)

# Save the result to a CSV file
aggregated_df.to_csv(output_file, index=False)

print("Aggregated CDN servers saved to:", output_file)
