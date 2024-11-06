import pandas as pd
import os

# File paths
websites_file_path = 'final_websites.csv'
raw_data_folder = 'raw_data'
output_file_path = 'final_websites_cdnservs_column.csv'

# Read all websites in order
websites_df = pd.read_csv(websites_file_path)
websites = websites_df['Website'].tolist() 

# Dictionary to store each website's CDN servers
cdn_servers_dict = {website: set() for website in websites}

# Iterate over each CSV file in the raw_data folder
for filename in os.listdir(raw_data_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(raw_data_folder, filename)
        df = pd.read_csv(file_path)
        
        # Iterate over each row and add cdn_server to the corresponding website
        for _, row in df.iterrows():
            website = row['Website']
            cdn_server = row['CDN Server']
            # Skip records where cdn_server is "Error"
            if website in cdn_servers_dict and cdn_server != "Error":
                cdn_servers_dict[website].add(cdn_server)

# Dictionary to store data for output
expanded_data = {'Website': []}
max_cdn_count = 0

# Fill data in the order of final_websites.csv
for website in websites:
    cdn_servers = list(cdn_servers_dict[website])
    # Process the website only if the number of cdn_servers is greater than 8
    if len(cdn_servers) > 8:
        expanded_data['Website'].append(website)
        max_cdn_count = max(max_cdn_count, len(cdn_servers))
        # Add CDN servers to respective columns
        for i, cdn_server in enumerate(cdn_servers):
            column_name = f'CDN_Server_{i + 1}'
            if column_name not in expanded_data:
                expanded_data[column_name] = []
            expanded_data[column_name].append(cdn_server)
        # Fill empty columns
        for j in range(len(cdn_servers), max_cdn_count):
            column_name = f'CDN_Server_{j + 1}'
            expanded_data[column_name].append(None)

# Convert to DataFrame and save to CSV file
expanded_df = pd.DataFrame(expanded_data)
expanded_df.to_csv(output_file_path, index=False)

print(f"Expanded data saved in original order to: {output_file_path}")
