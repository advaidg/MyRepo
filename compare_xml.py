import xml.etree.ElementTree as ET
import collections

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def xml_to_dict(element, skip_tags=None, key_tags=None, target_entity=None):
    """
    Convert an XML element and its children into a dictionary.
    For target_entity, convert it using composite keys from key_tags.
    """
    if skip_tags is None:
        skip_tags = []

    if key_tags is None:
        key_tags = []

    if element.tag in skip_tags:
        return None

    if len(element) == 0:
        return element.text

    data_dict = collections.OrderedDict()
    if element.tag == target_entity:
        key_values = tuple(element.find(tag).text for tag in key_tags if element.find(tag) is not None)
        data_dict[key_values] = element_to_dict(element, skip_tags)
    else:
        for child in element:
            if child.tag in skip_tags:
                continue

            child_dict = xml_to_dict(child, skip_tags, key_tags, target_entity)
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

def element_to_dict(element, skip_tags):
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

        child_dict = element_to_dict(child, skip_tags)
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

def compare_dicts(d1, d2, path=''):
    """
    Compare two dictionaries and print the differences.
    """
    differences = []
    
    if isinstance(d1, collections.OrderedDict) and isinstance(d2, collections.OrderedDict):
        keys1 = list(d1.keys())
        keys2 = list(d2.keys())
        if keys1 != keys2:
            differences.append(f"Different keys at {path}: {keys1} != {keys2}")
        for key in set(keys1) | set(keys2):
            if key not in d1:
                differences.append(f"Key {key} missing in first dict at {path}")
            elif key not in d2:
                differences.append(f"Key {key} missing in second dict at {path}")
            else:
                differences.extend(compare_dicts(d1[key], d2[key], path + '/' + str(key)))
    elif isinstance(d1, list) and isinstance(d2, list):
        if len(d1) != len(d2):
            differences.append(f"Different number of elements at {path}: {len(d1)} != {len(d2)}")
        for index, (item1, item2) in enumerate(zip(d1, d2)):
            differences.extend(compare_dicts(item1, item2, path + f'[{index}]'))
        if len(d1) > len(d2):
            for index in range(len(d2), len(d1)):
                differences.append(f"Extra element in first list at {path}[{index}]: {d1[index]}")
        elif len(d2) > len(d1):
            for index in range(len(d1), len(d2)):
                differences.append(f"Extra element in second list at {path}[{index}]: {d2[index]}")
    else:
        if d1 != d2:
            differences.append(f"Different values at {path}: {d1} != {d2}")
    
    return differences

def compare_xml_files(file1, file2, skip_tags=None, key_tags=None, target_entity=None):
    root1 = parse_xml(file1)
    root2 = parse_xml(file2)

    dict1 = xml_to_dict(root1, skip_tags, key_tags, target_entity)
    dict2 = xml_to_dict(root2, skip_tags, key_tags, target_entity)

    differences = compare_dicts(dict1, dict2)
    
    if not differences:
        print("The XML files are identical.")
    else:
        print("The XML files are different. Differences:")
        for diff in differences:
            print(diff)

# Example usage:
file1 = 'path_to_first_xml.xml'
file2 = 'path_to_second_xml.xml'
skip_tags = ['tag_to_skip1', 'tag_to_skip2']  # Add the tags you want to skip here
key_tags = ['', '']  # Add the tags to be used as composite keys here
target_entity = ''  # Specify the target entity tag here

compare_xml_files(file1, file2, skip_tags, key_tags, target_entity)
