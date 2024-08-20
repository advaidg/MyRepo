import re
from datetime import datetime

# Define the input and output file paths
input_file_path = 'input_file.txt'  # Replace with your input file path
output_file_path = 'output_file.sql'  # The SQL file where we'll save the INSERT statements

# Get the current date in the format 23-JAN-24
current_date = datetime.now().strftime("%d-%b-%y").upper()

# Open the input file and process each line
with open(input_file_path, 'r') as file, open(output_file_path, 'w') as sqlfile:
    for line in file:
        # Extract 1234, D1.D2, and the value "2"
        match = re.match(r'(\d+):[A-Z]+\.(D\d\.\D\d)\.\d+', line)
        if match:
            first_value = match.group(1)
            second_value = match.group(2)
            third_value = '2'  # This is a fixed value as per your requirement

            # Create the INSERT statement
            insert_statement = f"INSERT INTO your_table_name (COL1, COL2, COL3, COL4) VALUES ('{first_value}', '{second_value}', '{third_value}', '{current_date}');\n"
            
            # Write the INSERT statement to the SQL file
            sqlfile.write(insert_statement)

print(f"SQL INSERT statements have been generated and written to {output_file_path}")
