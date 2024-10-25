import requests
import socket
import pandas as pd
import os
import subprocess
#from tranco import Tranco

DC_Location = os.getenv('DC_Location')

#DC_Location = 'test_auto'  # Example value for testing

def get_top_websites(limit=15000):
    t = Tranco(cache=True, cache_dir='.tranco')
    latest_list = t.list().top(limit)  # probably add a date here for reproducibility
    return latest_list

def ping_websites(websites):
    data = []
    for website in websites:
        try:
            ip_address = socket.gethostbyname(website)
            cdn_server = socket.gethostbyaddr(ip_address)[0]
            data.append({'Website': website, 'IP Address': ip_address, 'CDN Server': cdn_server})
        except (requests.RequestException, socket.error) as e:
            data.append({'Website': website, 'IP Address': 'Error', 'CDN Server': 'Error'})
    
    df = pd.DataFrame(data)
    return df

def push_new_document(document_name):
    try:
        # Navigate to your repository directory
        subprocess.run(["git", "pull"], check=True)
        # Stage the new document
        subprocess.run(["git", "add", document_name], check=True)
        # Commit the changes
        subprocess.run(["git", "commit", "-m", "ScraperFinished"], check=True)
        # Push to the repository
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("New document pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    #websites = get_top_websites(10000)  # Get top 1000 websites
    websites_df = pd.read_csv('final_websites.csv') # Read the CSV file
    websites = websites_df['Website'].tolist()
    cdnservs = ping_websites(websites)
    name_of_file = f'cdnservs_{DC_Location}.csv'
    cdnservs.to_csv(name_of_file, index=False)
    push_new_document(name_of_file)
    #print(cdnservs.head())
