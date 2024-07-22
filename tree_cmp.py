import xml.etree.ElementTree as ET
from collections import defaultdict

def get_structure(element, path=""):
    structure = []
    children = list(element)
    current_path = path + "/" + element.tag
    structure.append(current_path)
    for child in children:
        structure.extend(get_structure(child, current_path))
    return structure

def compare_structures(struct1, struct2):
    set1 = set(struct1)
    set2 = set(struct2)

    only_in_first = set1 - set2
    only_in_second = set2 - set1

    return only_in_first, only_in_second

def print_differences(only_in_first, only_in_second):
    if only_in_first:
        print("Elements only in the first XML:")
        for item in sorted(only_in_first):
            print(item)
    else:
        print("No unique elements in the first XML.")

    if only_in_second:
        print("Elements only in the second XML:")
        for item in sorted(only_in_second):
            print(item)
    else:
        print("No unique elements in the second XML.")

def main(file1, file2):
    tree1 = ET.parse(file1)
    root1 = tree1.getroot()
    structure1 = get_structure(root1)

    tree2 = ET.parse(file2)
    root2 = tree2.getroot()
    structure2 = get_structure(root2)

    only_in_first, only_in_second = compare_structures(structure1, structure2)

    print_differences(only_in_first, only_in_second)

if __name__ == "__main__":
    file1 = "file1.xml"  # Replace with your XML file path
    file2 = "file2.xml"  # Replace with your XML file path

    main(file1, file2)
