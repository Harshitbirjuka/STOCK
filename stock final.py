#first download the close value csv file then download the open_int csv file

import csv
import pandas as pd
import os


# Specify the folder path where CSV files are located
folder_path = 'D:\stock csv'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

if csv_files:
    # Get the most recent CSV file
    latest_csv = max(csv_files, key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))
    
    # Construct the full path to the CSV file
    csv_file_path = os.path.join(folder_path, latest_csv)
    
    # Read the CSV file using Pandas
    data = pd.read_csv(csv_file_path)
    
   









# Filter data for option type CE
ce_data = data[data['OPTION_TYP'] == 'CE']
ce_max_open_int = ce_data.groupby('SYMBOL')['OPEN_INT'].idxmax()
max_ce_data = ce_data.loc[ce_max_open_int]

# Filter data for option type PE
pe_data = data[data['OPTION_TYP'] == 'PE']
pe_max_open_int = pe_data.groupby('SYMBOL')['OPEN_INT'].idxmax()
max_pe_data = pe_data.loc[pe_max_open_int]

# Concatenate the data for CE and PE option types
output_data = pd.concat([max_ce_data, max_pe_data])

# Save the output data to a new CSV file
output_data.to_csv('highest_open_int_data.csv', index=False)

print("Data saved to 'highest_open_int_data.csv'")


    


import os

folder_path = 'D:\stock csv'
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

if len(csv_files) >= 2:
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    second_latest_csv = csv_files[1]
    print("Second Latest CSV file:", second_latest_csv)
elif len(csv_files) == 1:
    print("Only one CSV file found in the folder.")
else:
    print("No CSV files found in the folder.")

folder_path = 'D:/stock csv'

# Get the absolute file paths
close_file_path = os.path.join(folder_path, second_latest_csv)






# Read the first CSV template
with open('highest_open_int_data.csv', 'r') as template_file:
    template_reader = csv.DictReader(template_file)
    template_data = list(template_reader)

# Read the second CSV file containing the "close" values
with open(close_file_path, 'r') as close_file:
    close_reader = csv.DictReader(close_file)
    close_data = list(close_reader)

# Filter data from the second CSV file for series 'EQ'
close_data_eq_series = [row for row in close_data if row['SERIES'] == 'EQ']

# Create a dictionary to store strike price ranges for each symbol
strike_price_ranges = {}
for row in template_data:
    symbol = row['SYMBOL']
    strike_pr = float(row['STRIKE_PR'])
    if symbol not in strike_price_ranges:
        strike_price_ranges[symbol] = []
    strike_price_ranges[symbol].append(strike_pr)

# Collect matching rows and close values
matching_rows_with_close = []

# Process the "close" values and compare with strike price ranges
for row in close_data_eq_series:
    symbol = row['SYMBOL']
    close = float(row['CLOSE'])
    
    if symbol in strike_price_ranges:
        strike_prices = strike_price_ranges[symbol]
        min_strike = min(strike_prices)
        max_strike = max(strike_prices)
        
        if close < min_strike or close > max_strike:
            matching_rows = [r for r in template_data if r['SYMBOL'] == symbol]
            pe_strike_pr = next((r['STRIKE_PR'] for r in matching_rows if r['OPTION_TYP'] == 'PE'), None)
            
            if pe_strike_pr is not None:
                ce_strike_pr = next((r['STRIKE_PR'] for r in matching_rows if r['OPTION_TYP'] == 'CE'), None)
                
                ce_open_int = next((r['OPEN_INT'] for r in matching_rows if r['OPTION_TYP'] == 'CE'), None)
                pe_open_int = next((r['OPEN_INT'] for r in matching_rows if r['OPTION_TYP'] == 'PE'), None)
                
                ce_close = close if close > float(pe_strike_pr) else ''
                pe_close = close if close <= float(pe_strike_pr) else ''
                
                matching_row = [
                    symbol,
                    ce_strike_pr,
                    ce_open_int,
                    ce_close,
                    pe_strike_pr,
                    pe_open_int,
                    pe_close
                ]
                
                matching_rows_with_close.append(matching_row)

# Write the matching data to an output CSV file
output_file = 'output.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['symbol', 'CE_strike_pr', 'CE_open_int', 'CE_close', 'PE_strike_pr', 'PE_open_int', 'PE_close'])
    for row_data in matching_rows_with_close:
        writer.writerow(row_data)

print("Output written to", output_file)



