import xml.etree.ElementTree as ET

def sort_xml_recursive(element, order='ascending'):
    element[:] = sorted(element, key=lambda child: child.tag, reverse=(order == 'descending'))
    for child in element:
        sort_xml_recursive(child, order)

def sort_xml_elements(xml_file, order='ascending'):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    sort_xml_recursive(root, order)

    # Save the modified XML to a new file or overwrite the original
    tree.write('sorted_' + xml_file)

# Replace 'your_file.xml' with the actual name of your XML file
sort_xml_elements('your_file.xml', order='ascending')
