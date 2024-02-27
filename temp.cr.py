import tempfile
import shutil

# Specify the dynamic value you want to set
new_value = 4

# Read the original configuration file
config_file_path = 'config.txt'
with open(config_file_path, 'r') as original_file:
    lines = original_file.readlines()

# Modify the value in memory
for i, line in enumerate(lines):
    if 'dataElements:' in line:
        lines[i] = f'dataElements: {new_value}\n'

# Create a temporary directory and file
temp_dir = tempfile.mkdtemp()
temp_config_path = f'{temp_dir}/temp_config.txt'

# Write the modified content to the temporary file
with open(temp_config_path, 'w') as temp_file:
    temp_file.writelines(lines)

# Run your Java application with the temporary configuration
java_command = f'java -jar your-application.jar -Dconfig.file={temp_config_path}'
# Use subprocess or os.system to run the command, e.g., subprocess.run(java_command, shell=True)

# Clean up the temporary directory
shutil.rmtree(temp_dir)
