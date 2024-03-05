import xml.etree.ElementTree as ET

def sort_xml_elements(xml_file, entity_tag, order='ascending'):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the entity to sort
    entities = root.findall(".//{}".format(entity_tag))

    if entities:
        # Sort the entities based on the account number attribute
        entities.sort(key=lambda entity: entity.get('accountnumber'), reverse=(order == 'descending'))
    else:
        print("No entities with tag '{}' found in the XML file.".format(entity_tag))
        return

    # Save the modified XML to a new file or overwrite the original
    tree.write('sorted_' + xml_file)

# Replace 'your_file.xml' with the actual name of your XML file
# Replace 'AccountEntity' with the tag of the entity you want to sort
sort_xml_elements('your_file.xml', entity_tag='AccountEntity', order='ascending')
