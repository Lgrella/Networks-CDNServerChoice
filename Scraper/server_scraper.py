import requests
import socket
import pandas as pd
from tranco import Tranco

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


# Example usage
if __name__ == "__main__":
    websites = get_top_websites(10)  # Get top 10 websites for testing
    cdnservs = ping_websites(websites)
    #print(cdnservs.head())