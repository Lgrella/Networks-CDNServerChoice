import requests
import socket
import pandas as pd
from tranco import Tranco

# def get_top_websites(limit=15000):
#     t = Tranco(cache=True, cache_dir='.tranco')
#     latest_list = t.list().top(limit)  # probably add a date here for reproducibility
#     return latest_list

# def ping_websites(websites):
#     data = []
#     for website in websites:
#         try:
#             ip_address = socket.gethostbyname(website)
#             cdn_server = socket.gethostbyaddr(ip_address)[0]
#             data.append({'Website': website, 'IP Address': ip_address, 'CDN Server': cdn_server})
#         except (requests.RequestException, socket.error) as e:
#             data.append({'Website': website, 'IP Address': 'Error', 'CDN Server': 'Error'})
    
#     df = pd.DataFrame(data)
#     return df


# # Example usage
# if __name__ == "__main__":
#     websites = get_top_websites(10000)  # Get top 1000 websites
#     cdnservs = ping_websites(websites)
#     cdnservs.to_csv('banglore_top10000.csv', index=False)
#     #print(cdnservs.head())

def get_top_websites(limit=15000):
    t = Tranco(cache=True, cache_dir='.tranco')
    latest_list = t.list().top(limit)
    return latest_list

def ping_websites_and_write(websites, output_file):
    with open(output_file, 'w') as f:
        f.write('Website,IP Address,CDN Server\n')

    for website in websites:
        try:
            ip_address = socket.gethostbyname(website)
            cdn_server = socket.gethostbyaddr(ip_address)[0]
            row = {'Website': website, 'IP Address': ip_address, 'CDN Server': cdn_server}
        except (requests.RequestException, socket.error) as e:
            row = {'Website': website, 'IP Address': 'Error', 'CDN Server': 'Error'}

        df = pd.DataFrame([row])
        df.to_csv(output_file, mode='a', header=False, index=False)
        # print("saved")

if __name__ == "__main__":
    output_file = 'singapore_top10000.csv'
    websites = get_top_websites(10000)
    ping_websites_and_write(websites, output_file)