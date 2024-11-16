import os
import csv

raw_data_folder = './raw_data'
cdn_file = './final_websites_cdnservs.csv'
output_file = './final_websites_cdnservs_ip.csv'

output_columns = ['Website'] + [f'CDN_Server_{i}' for i in range(1, 14)] + [f'IP{i}' for i in range(1, 14)]

with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=output_columns)
    writer.writeheader()

    with open(cdn_file, 'r') as cdn_f:
        reader = csv.DictReader(cdn_f)
        for cdn_server in reader:
            result_row = {'Website': cdn_server['Website']}
            for i in range(1, 14):  
                cdn_col = f'CDN_Server_{i}'
                cdn_name = cdn_server.get(cdn_col, 'None')  
                ip_address = None

                if cdn_name and cdn_name != 'None':  
                    for raw_file in os.listdir(raw_data_folder):
                        if raw_file.endswith('.csv'):
                            with open(os.path.join(raw_data_folder, raw_file), 'r') as raw_f:
                                raw_reader = csv.DictReader(raw_f)
                                for row in raw_reader:
                                    if cdn_name == row['CDN Server']:
                                        ip_address = row['IP Address']
                                        break
                            if ip_address: 
                                break

                result_row[cdn_col] = cdn_name
                result_row[f'IP{i}'] = ip_address if ip_address else ''

            writer.writerow(result_row)
            print(f"Processed and saved record for {cdn_server['Website']}")

print(f"CDN server IPs saved to {output_file}")
