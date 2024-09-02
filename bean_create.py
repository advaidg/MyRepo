import xml.etree.ElementTree as ET

# Define mappings from XML configuration to Java annotations and types
bean_mapping = {
    "bean": "@Bean",
    "property": "Property",
    "constructor-arg": "ConstructorArg"
}

def convert_bean_to_java(bean_element):
    """Convert a single bean XML element to a Java method."""
    bean_id = bean_element.get("id")
    bean_class = bean_element.get("class")

    java_method = f"@Bean\npublic {bean_class} {bean_id}() {{\n"
    java_method += f"    return new {bean_class}("
    
    # Check for constructor arguments
    constructor_args = bean_element.findall("constructor-arg")
    if constructor_args:
        args = []
        for arg in constructor_args:
            value = arg.get("value")
            ref = arg.get("ref")
            if value:
                args.append(f'"{value}"')
            elif ref:
                args.append(f"{ref}()")
        java_method += ", ".join(args)
    
    java_method += ");\n"

    # Check for properties to be set via setter methods
    properties = bean_element.findall("property")
    if properties:
        for prop in properties:
            name = prop.get("name")
            value = prop.get("value")
            ref = prop.get("ref")
            if value:
                java_method += f"    {bean_id}.set{name.capitalize()}(\"{value}\");\n"
            elif ref:
                java_method += f"    {bean_id}.set{name.capitalize()}({ref}());\n"

    java_method += "}\n"
    return java_method

def convert_xml_to_java_config(xml_file, output_file):
    """Convert the given XML configuration to Java configuration."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(output_file, "w") as java_file:
        java_file.write("import org.springframework.context.annotation.Bean;\n")
        java_file.write("import org.springframework.context.annotation.Configuration;\n\n")
        java_file.write("@Configuration\n")
        java_file.write("public class AppConfig {\n\n")

        for bean in root.findall("bean"):
            java_bean = convert_bean_to_java(bean)
            java_file.write(java_bean + "\n")

        java_file.write("}\n")

if __name__ == "__main__":
    xml_input_file = "application-context.xml"
    java_output_file = "AppConfig.java"
    convert_xml_to_java_config(xml_input_file, java_output_file)
    print(f"Java configuration has been written to {java_output_file}")
