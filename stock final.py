import csv
import pandas as pd
import os

# Specify the folder path where CSV files are located
folder_path = 'D:/stock csv'

# Read the first CSV template
template_file_path = 'highest_open_int_data.csv'
template_data = pd.read_csv(template_file_path)

# Get the second latest CSV file
csv_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.csv')]

if len(csv_files) >= 2:
    csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
    second_latest_csv = csv_files[1]
else:
    print("There are not enough CSV files in the folder.")
    exit()

# Read the second CSV file containing the "close" values
close_file_path = os.path.join(folder_path, second_latest_csv)
close_data = pd.read_csv(close_file_path)

# Filter data from the second CSV file for series 'EQ'
close_data_eq_series = close_data[close_data['SERIES'] == 'EQ']

# Create a dictionary to store strike price ranges for each symbol
strike_price_ranges = {}
for _, row in template_data.iterrows():
    symbol = row['SYMBOL']
    strike_pr = float(row['STRIKE_PR'])
    if symbol not in strike_price_ranges:
        strike_price_ranges[symbol] = []
    strike_price_ranges[symbol].append(strike_pr)

# Collect matching rows and close values
matching_rows_with_close = []

# Process the "close" values and compare with strike price ranges
for _, row in close_data_eq_series.iterrows():
    symbol = row['SYMBOL']
    close = float(row['CLOSE'])
    
    if symbol in strike_price_ranges:
        strike_prices = strike_price_ranges[symbol]
        min_strike = min(strike_prices)
        max_strike = max(strike_prices)
        
        matching_rows = [r for r in template_data[template_data['SYMBOL'] == symbol].itertuples()]
        
        pe_strike_pr = next((r.STRIKE_PR for r in matching_rows if r.OPTION_TYP == 'PE'), None)
        ce_strike_pr = next((r.STRIKE_PR for r in matching_rows if r.OPTION_TYP == 'CE'), None)
        
        ce_open_int = next((r.OPEN_INT for r in matching_rows if r.OPTION_TYP == 'CE'), None)
        pe_open_int = next((r.OPEN_INT for r in matching_rows if r.OPTION_TYP == 'PE'), None)
        
        ce_close = close if close > ce_strike_pr else ''
        pe_close = close if close < pe_strike_pr else ''
        
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
    writer.writerows(matching_rows_with_close)

print("Output written to", output_file)

