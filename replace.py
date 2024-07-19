def replace_characters_in_file(input_file, output_file, start_pos, end_pos, replacement_text):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            if len(line) >= end_pos:
                line = line[:start_pos] + replacement_text + line[end_pos:]
            file.write(line)

# Replace 'input.txt' with the path to your input file and 'output.txt' with the desired output file path
input_file = 'input.txt'
output_file = 'output.txt'
start_pos = 608  # 609th character (0-indexed)
end_pos = 616  # 617th character (0-indexed)
replacement_text = 'NEW_TEXT'  # Replace this with your desired replacement text

replace_characters_in_file(input_file, output_file, start_pos, end_pos, replacement_text)
