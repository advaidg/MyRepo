import os
import re

def parse_record(line):
    parts = re.split(r"\s+", line.strip())
    line_info = parts[2]
    file_info = parts[4]

    line_number = int(line_info.replace("Line", ""))
    file_number = int(file_info.replace("file", "").replace(":", ""))
    franchise_name = parts[5]
    account_number = parts[6]

    return line_number, file_number, franchise_name, account_number

def read_and_split_file(input_file):
    file1_records = {}
    file2_records = {}

    with open(input_file, "r") as f:
        for line in f:
            if line.startswith("Non Matching"):
                line_number, file_number, franchise_name, account_number = parse_record(line)
                if file_number == 1:
                    file1_records[account_number] = (line_number, line)
                elif file_number == 2:
                    file2_records[account_number] = (line_number, line)

    return file1_records, file2_records

def write_sorted_files(file1_records, file2_records, output_dir, distributor_id, file_type):
    file1_name = f"error_{distributor_id}_{file_type}_file1.dat"
    file2_name = f"error_{distributor_id}_{file_type}_file2.dat"

    file1_path = os.path.join(output_dir, file1_name)
    file2_path = os.path.join(output_dir, file2_name)

    all_account_numbers = sorted(set(file1_records.keys()).union(set(file2_records.keys())))

    with open(file1_path, "w") as file1, open(file2_path, "w") as file2:
        for account_number in all_account_numbers:
            line1 = file1_records.get(account_number, ("", "\n"))[1]
            line2 = file2_records.get(account_number, ("", "\n"))[1]
            file1.write(line1)
            file2.write(line2)

    print(f"Created or replaced: {file1_path}")
    print(f"Created or replaced: {file2_path}")

def main():
    filename = input("Enter the filename (e.g., error_123456_account.dat): ")
    input_dir = "/home/pgajana/testing"
    output_base_dir = "/home/pgajana/output"

    match = re.match(r"error_(\d+)_(\w+)\.dat", filename)

    if not match:
        print("Filename does not match the expected pattern: error_distributorId_filetype.dat")
        return

    distributor_id = match.group(1)
    file_type = match.group(2)

    output_dir = os.path.join(output_base_dir, f"{distributor_id}_{file_type}")
    os.makedirs(output_dir, exist_ok=True)

    input_file = os.path.join(input_dir, filename)

    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    file1_records, file2_records = read_and_split_file(input_file)
    write_sorted_files(file1_records, file2_records, output_dir, distributor_id, file_type)

if __name__ == "__main__":
    main()
