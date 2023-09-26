import pandas as pd
import json

# Input Excel file path
excel_file = 'input.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(excel_file)

# Convert the DataFrame to a list of dictionaries, where each dictionary represents a row
data_list = df.to_dict(orient='records')

# Define the output JSON file path
output_json_file = 'output.json'

# Save the list of dictionaries as a JSON array in the output file
with open(output_json_file, 'w') as json_file:
    json.dump(data_list, json_file, indent=4)

print(f"Data from '{excel_file}' has been converted and saved to '{output_json_file}'.")
