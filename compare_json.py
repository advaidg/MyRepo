import json
from deepdiff import DeepDiff

def remove_elements(data, keys_to_remove):
    """
    Remove specified keys from the dictionary recursively.
    """
    if isinstance(data, list):
        for item in data:
            remove_elements(item, keys_to_remove)
    elif isinstance(data, dict):
        for key in keys_to_remove:
            if key in data:
                del data[key]
        for value in data.values():
            remove_elements(value, keys_to_remove)

def load_json(file_path):
    """
    Load JSON data from a file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    """
    Save JSON data to a file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def compare_jsons(file1, file2, keys_to_remove):
    """
    Compare two JSON files after removing specified keys.
    """
    # Load JSON files
    json1 = load_json(file1)
    json2 = load_json(file2)
    
    # Remove specified elements
    remove_elements(json1, keys_to_remove)
    remove_elements(json2, keys_to_remove)

    # Save modified JSON files for inspection (optional)
    save_json('modified_' + file1, json1)
    save_json('modified_' + file2, json2)

    # Compare JSON data
    diff = DeepDiff(json1, json2, ignore_order=True)
    
    if diff:
        print("Differences found:")
        print(json.dumps(diff, indent=4))
    else:
        print("No differences found. The JSON files are equivalent after removing specified elements.")

if __name__ == "__main__":
    file1 = 'file1.json'  # Replace with your JSON file path
    file2 = 'file2.json'  # Replace with your JSON file path
    keys_to_remove = ['timestamp', 'id']  # Replace with keys to remove before comparison
    
    compare_jsons(file1, file2, keys_to_remove)
