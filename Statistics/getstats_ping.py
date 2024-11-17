import socket
import pandas as pd
import numpy as np
import subprocess
import csv

# Load the data from your CSV or dataframe
data = pd.read_csv('Scraper/final_websites_cdnservs_ip.csv')

#restrict to 5 records and keep only columns that start with ip and the website column;

filtered_data = data.loc[:, data.columns.str.contains("Website|IP")]
filtered_data = filtered_data.head(1)
# Function to ping a host and return latency stats
def ping_host(host, count=10):
    #print(f"Pinging {host}...")
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Extract round-trip times (RTTs) from the output
        rtts = [
            float(line.split("time=")[-1].split(" ")[0])
            for line in result.stdout.splitlines()
            if "time=" in line
        ]
        if rtts:
            return {
                "min": np.min(rtts),
                "max": np.max(rtts),
                "mean": np.mean(rtts),
                "median": np.median(rtts)
            }
        else:
            return None
    except Exception as e:
        #print(f"Error pinging {host}: {e}")
        return None


# Process each website in the dataframe
results = []
for index, row in filtered_data.iterrows():
    website = row['Website']
    cdn_servers = row[1:].dropna().tolist()
    print(f"Processing {website} with {len(cdn_servers)} CDN servers")

    # Resolve IP address for website to find active CDN server
    try:
        ip_address = socket.gethostbyname(website)
        cdn_server = socket.gethostbyaddr(ip_address)[0]
        cdn_servers.insert(0, ip_address)  # Place the active CDN server at the beginning
        #print(f"Resolved {website} to {ip_address} ({cdn_server})")
    except Exception as e:
        #print(f"Error resolving {website}: {e}")
        continue

    # Ping each CDN server and collect stats
    for cdn in cdn_servers:
        stats = ping_host(cdn)
        if stats:
            results.append({
                "website": website,
                "cdn": cdn,
                **stats
            })

# Save results to CSV
output_df = pd.DataFrame(results)
output_df.to_csv('Statistics/cdn_ping_stats.csv', index=False)

print("Ping statistics saved to cdn_ping_stats.csv")
