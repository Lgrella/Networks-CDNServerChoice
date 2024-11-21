import socket
import ssl
import time
import pandas as pd

def measure_response_time(domain, ip, port=443, use_ssl=True):
    """
    Measures response time when connecting to a specific IP for a domain.
    """
    try:
        start_time = time.time()
        sock = socket.create_connection((ip, port), timeout=5)
        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=domain)
        request = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())
        sock.recv(1024)
        end_time = time.time()
        return end_time - start_time
    except Exception as e:
        print(f"Error connecting to {ip} for domain {domain}: {e}")
        return None
    finally:
        if 'sock' in locals():
            sock.close()

def process_csv(input_file, output_file):
    """
    Process the input CSV to compare performance metrics and write results to an output CSV.
    """
    results = []

    # Read input CSV
    df = pd.read_csv(input_file)

    for _, row in df.iterrows():
        if not row['CDNChoiceGood']:  # Only process rows with CDNChoiceGood = False
            cdn_first_ip = row['cdn_first']
            cdn_min_median_ip = row['cdn_min_median']
            domain = row['website']  # Use the website column for the domain name

            
            response_time_first = measure_response_time(domain, cdn_first_ip)
            response_time_min_median = measure_response_time(domain, cdn_min_median_ip)

            
            throughput_first = 1 / response_time_first if response_time_first else None
            throughput_min_median = 1 / response_time_min_median if response_time_min_median else None

            
            latency_diff = response_time_first - response_time_min_median if response_time_first and response_time_min_median else None

            # Append results to the list
            results.append({
                'website': domain,
                'cdn_first': cdn_first_ip,
                'cdn_min_median': cdn_min_median_ip,
                'response_time_first': response_time_first,
                'response_time_min_median': response_time_min_median,
                'throughput_first': throughput_first,
                'throughput_min_median': throughput_min_median,
                'latency_diff': latency_diff,
            })

    # Write results to output CSV
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_file, index=False)

# File paths
input_csv = 'sgp_compare.csv'
output_csv = 'sgp_processed_data.csv'

# Process the CSV
process_csv(input_csv, output_csv)
