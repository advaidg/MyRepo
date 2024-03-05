import xml.etree.ElementTree as ET

def sort_xml_elements(xml_file, entity_to_sort, order='ascending'):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the entity to sort
    entity = root.find(".//{}".format(entity_to_sort))

    if entity is not None:
        # Sort the child elements of the specified entity
        entity[:] = sorted(entity, key=lambda child: child.tag, reverse=(order == 'descending'))
    else:
        print("Entity '{}' not found in the XML file.".format(entity_to_sort))
        return

    # Save the modified XML to a new file or overwrite the original
    tree.write('sorted_' + xml_file)

# Replace 'your_file.xml' with the actual name of your XML file
# Replace 'EntityToSort' with the tag of the entity you want to sort
sort_xml_elements('your_file.xml', entity_to_sort='EntityToSort', order='ascending')
