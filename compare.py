import csv

# Function to read CSV file and return a list of dictionaries
def read_csv(file_path):
    data = []
    with open(file_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Function to write a list of dictionaries to a CSV file
def write_csv(file_path, data):
    with open(file_path, 'wb') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)

# Load the CSV files into lists of dictionaries
file1_path = 'path/to/your/file1.csv'
file2_path = 'path/to/your/file2.csv'

data1 = read_csv(file1_path)
data2 = read_csv(file2_path)

# Compare the two datasets
differences = []

for row in data1:
    if row not in data2:
        differences.append(row)

for row in data2:
    if row not in data1:
        differences.append(row)

# Save the differences to a new CSV file
output_file_path = 'path/to/your/output/differences.csv'
write_csv(output_file_path, differences)

print("Differences have been saved to:", output_file_path)
