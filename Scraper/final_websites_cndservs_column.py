import os
import pandas as pd
import whois
import re
import csv

# List of CDN providers based on the image
cdn_providers = [
    "cloudflare", "keycdn", "stackpath", "fastly", "akamai", "gcore",
    "imperva", "advancedhosting", "chinacache", "cdnvideo",
    "cdn77", "cachefly", "bunnycdn", "leaseweb", "belugacdn",
    "kingsoft", "limelight", "edgio", "sucuri", "bootstrapcdn", "cdnetworks", "cloudfront"
]

# Function to determine if the server is a CDN server
def is_cdn_server(server_name, server_ip):
    server_name_lower = server_name.lower()

    if "cdn" in server_name_lower or "edge" in server_name_lower:
        return True

    for provider in cdn_providers:
        if provider.lower() in server_name_lower:
            return True

    # # Perform WHOIS lookup using python-whois library
    # try:
    #     whois_info = whois.whois(server_ip)
    #     organization = whois_info.org if whois_info.org else ""
    #     # print(f"organization is {organization}")
        
    #     # Check if the organization matches any CDN provider
    #     for provider in cdn_providers:
    #         if provider.lower() in organization.lower():
    #             return True

    # except Exception as e:
    #     print(f"WHOIS lookup failed for {server_ip}")

    return False

# File paths
websites_file_path = 'final_websites.csv'
raw_data_folder = 'raw_data'
output_file_path = 'final_websites_cdnservs.csv'

# Read all websites in the list
websites_df = pd.read_csv(websites_file_path)
websites = websites_df['Website'].tolist() 

# Create a dictionary to store each website's CDN servers
cdn_servers_dict = {website: set() for website in websites}

# Iterate over each CSV file in the raw_data folder
for filename in os.listdir(raw_data_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(raw_data_folder, filename)
        df = pd.read_csv(file_path)
        
        # Iterate over each row and add the CDN server to the corresponding website
        for _, row in df.iterrows():
            website = row['Website']
            cdn_server = row['CDN Server']
            server_ip = row.get('IP Address', None) 

            # Skip records where cdn_server is "Error"
            if website in cdn_servers_dict and cdn_server != "Error":
                # Check if it is a CDN server
                if is_cdn_server(cdn_server, server_ip):
                    cdn_servers_dict[website].add(cdn_server)
        # Print confirmation after processing each CSV file
        print(f"Processed file: {filename}")

# Dictionary to store data for output
expanded_data = {'Website': []}
max_cdn_count = 13

# Initialize expanded_data with empty lists for Website and each CDN server column
expanded_data = {'Website': []}
for i in range(max_cdn_count):
    expanded_data[f'CDN_Server_{i + 1}'] = []

# Fill data in the order of final_websites.csv
for website in websites:
    cdn_servers = list(cdn_servers_dict[website])
    if len(cdn_servers) > 6:  # Only include if there are more than 6 CDN servers
        expanded_data['Website'].append(website)
        
        # Add CDN servers to respective columns
        for i in range(max_cdn_count):
            if i < len(cdn_servers):
                expanded_data[f'CDN_Server_{i + 1}'].append(cdn_servers[i])
            else:
                expanded_data[f'CDN_Server_{i + 1}'].append(None)  # Fill with None if fewer servers

# Convert to DataFrame and save to CSV file
expanded_df = pd.DataFrame(expanded_data)
expanded_df.to_csv(output_file_path, index=False)

print(f"Expanded data saved to: {output_file_path}")
# print(is_cdn_server('	media-router-aol71.canaryp.media.vip.ir2.yahoo.com', '188.125.72.137'))
