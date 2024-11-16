# import os
# import csv

# # 定义文件路径
# raw_data_folder = './raw_data'
# cdn_file = './final_websites_cdnservs.csv'
# output_file = './final_websites_cdnservs_ip.csv'

# # 加载 CDN server 列表
# cdn_servers = []
# with open(cdn_file, 'r') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         cdn_servers.append(row)

# # 搜索 IP 地址并创建对应的结果
# results = []
# for cdn_server in cdn_servers:
#     result_row = {'Website': cdn_server['Website']}
#     for i in range(1, 14):  # 对应最多13个 CDN servers
#         cdn_col = f'CDN_Server_{i}'
#         cdn_name = cdn_server.get(cdn_col, 'None')  # 获取 CDN server，如果不存在则为 'None'
#         ip_address = None

#         # 在 raw_data 文件夹中查找对应的 IP 地址
#         if cdn_name and cdn_name != 'None':  # 只搜索非空和非 'None' 的 CDN server
#             for raw_file in os.listdir(raw_data_folder):
#                 if raw_file.endswith('.csv'):
#                     with open(os.path.join(raw_data_folder, raw_file), 'r') as f:
#                         reader = csv.DictReader(f)
#                         for row in reader:
#                             if cdn_name == row['CDN Server']:
#                                 ip_address = row['IP Address']
#                                 break
#                     if ip_address:  # 如果找到就停止搜索
#                         break

#         # 添加到结果中
#         result_row[cdn_col] = cdn_name
#         result_row[f'IP{i}'] = ip_address if ip_address else 'None'

#     results.append(result_row)

# # 写入结果到新的 CSV 文件
# output_columns = ['Website'] + [f'CDN_Server_{i}' for i in range(1, 14)] + [f'IP{i}' for i in range(1, 14)]
# with open(output_file, 'w', newline='') as f:
#     writer = csv.DictWriter(f, fieldnames=output_columns)
#     writer.writeheader()
#     writer.writerows(results)

# print(f"CDN server IPs saved to {output_file}")

import os
import csv

# 定义文件路径
raw_data_folder = './raw_data'
cdn_file = './final_websites_cdnservs.csv'
output_file = './final_websites_cdnservs_ip.csv'

# 定义输出列的标题
output_columns = ['Website'] + [f'CDN_Server_{i}' for i in range(1, 14)] + [f'IP{i}' for i in range(1, 14)]

# 打开输出文件并写入表头
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=output_columns)
    writer.writeheader()

    # 加载 CDN server 列表并处理每个网站的记录
    with open(cdn_file, 'r') as cdn_f:
        reader = csv.DictReader(cdn_f)
        for cdn_server in reader:
            result_row = {'Website': cdn_server['Website']}
            for i in range(1, 14):  # 对应最多13个 CDN servers
                cdn_col = f'CDN_Server_{i}'
                cdn_name = cdn_server.get(cdn_col, 'None')  # 获取 CDN server，如果不存在则为 'None'
                ip_address = None

                # 在 raw_data 文件夹中查找对应的 IP 地址
                if cdn_name and cdn_name != 'None':  # 只搜索非空和非 'None' 的 CDN server
                    for raw_file in os.listdir(raw_data_folder):
                        if raw_file.endswith('.csv'):
                            with open(os.path.join(raw_data_folder, raw_file), 'r') as raw_f:
                                raw_reader = csv.DictReader(raw_f)
                                for row in raw_reader:
                                    if cdn_name == row['CDN Server']:
                                        ip_address = row['IP Address']
                                        break
                            if ip_address:  # 如果找到就停止搜索
                                break

                # 添加到结果中
                result_row[cdn_col] = cdn_name
                result_row[f'IP{i}'] = ip_address if ip_address else 'None'

            # 写入单个网站的记录到输出文件
            writer.writerow(result_row)
            print(f"Processed and saved record for {cdn_server['Website']}")

print(f"CDN server IPs saved to {output_file}")
