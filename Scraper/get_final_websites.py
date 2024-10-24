import pandas as pd

# Read the CSV file
df = pd.read_csv('top10000.csv')

# Filter out rows where the second column is "Error"
filtered_df = df[df["CDN Server"] != 'Error']
#print(len(filtered_df)) #4,186

filtered_df2 = filtered_df[filtered_df["CDN Server"] != filtered_df["Website"]] #4007
filtered_df2_removed = filtered_df[filtered_df["CDN Server"] == filtered_df["Website"]] #removed 179

#print(len(filtered_df2))
#print(len(filtered_df2_removed))
# Save the filtered DataFrame to a new CSV file
filtered_df2.to_csv('final_websites.csv', index=True, header=True, columns=["Website"])