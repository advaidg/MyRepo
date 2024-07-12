import xml.etree.ElementTree as ET
import collections

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def xml_to_dict(element, skip_tags=None):
    """
    Convert an XML element and its children into a dictionary.
    """
    if skip_tags is None:
        skip_tags = []

    if element.tag in skip_tags:
        return None

    if len(element) == 0:
        return element.text

    data_dict = collections.OrderedDict()
    for child in element:
        if child.tag in skip_tags:
            continue

        child_dict = xml_to_dict(child, skip_tags)
        if child_dict is None:
            continue

        if child.tag not in data_dict:
            data_dict[child.tag] = child_dict
        else:
            if isinstance(data_dict[child.tag], list):
                data_dict[child.tag].append(child_dict)
            else:
                data_dict[child.tag] = [data_dict[child.tag], child_dict]

    return data_dict

def compare_dicts(d1, d2):
    """
    Compare two dictionaries and return a boolean indicating whether they are equal.
    """
    if isinstance(d1, collections.OrderedDict) and isinstance(d2, collections.OrderedDict):
        if len(d1) != len(d2):
            return False
        for k1, k2 in zip(sorted(d1.keys()), sorted(d2.keys())):
            if k1 != k2 or not compare_dicts(d1[k1], d2[k2]):
                return False
        return True
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            return False
        for item1, item2 in zip(sorted(d1, key=str), sorted(d2, key=str)):
            if not compare_dicts(item1, item2):
                return False
        return True
    else:
        return d1 == d2

def compare_xml_files(file1, file2, skip_tags=None):
    root1 = parse_xml(file1)
    root2 = parse_xml(file2)

    dict1 = xml_to_dict(root1, skip_tags)
    dict2 = xml_to_dict(root2, skip_tags)

    return compare_dicts(dict1, dict2)

# Example usage:
file1 = 'path_to_first_xml.xml'
file2 = 'path_to_second_xml.xml'
skip_tags = ['tag_to_skip1', 'tag_to_skip2']  # Add the tags you want to skip here

are_equal = compare_xml_files(file1, file2, skip_tags)
print(f"The XML files are {'identical' if are_equal else 'different'}.")
