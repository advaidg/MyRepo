import xml.etree.ElementTree as ET

def generate_java_method(bean_id, bean_class, constructor_args, properties):
    """
    Generates the Java method for the given bean configuration.
    """
    method = f"@Bean\npublic {bean_class} {bean_id}() {{\n"
    
    if constructor_args:
        args = ", ".join(constructor_args)
        method += f"    {bean_class} {bean_id} = new {bean_class}({args});\n"
    else:
        method += f"    {bean_class} {bean_id} = new {bean_class}();\n"
    
    for prop in properties:
        method += f"    {bean_id}.set{prop['name'].capitalize()}({prop['value']});\n"
    
    method += f"    return {bean_id};\n"
    method += "}\n"
    
    return method

def parse_constructor_args(bean_element):
    """
    Parses the constructor-arg elements of a bean and returns a list of arguments.
    """
    args = []
    for arg in bean_element.findall("constructor-arg"):
        value = arg.get("value")
        ref = arg.get("ref")
        if value:
            args.append(f'"{value}"')
        elif ref:
            args.append(f"{ref}()")
    return args

def parse_properties(bean_element):
    """
    Parses the property elements of a bean and returns a list of properties.
    """
    properties = []
    for prop in bean_element.findall("property"):
        prop_name = prop.get("name")
        value = prop.get("value")
        ref = prop.get("ref")
        if value:
            properties.append({"name": prop_name, "value": f'"{value}"'})
        elif ref:
            properties.append({"name": prop_name, "value": f"{ref}()"})
    return properties

def convert_xml_to_java_config(xml_file, output_file):
    """
    Converts the given Spring XML configuration file to Java configuration.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    with open(output_file, "w") as java_file:
        java_file.write("import org.springframework.context.annotation.Bean;\n")
        java_file.write("import org.springframework.context.annotation.Configuration;\n\n")
        java_file.write("@Configuration\n")
        java_file.write("public class AppConfig {\n\n")
        
        for bean in root.findall("bean"):
            bean_id = bean.get("id")
            bean_class = bean.get("class")
            constructor_args = parse_constructor_args(bean)
            properties = parse_properties(bean)
            java_method = generate_java_method(bean_id, bean_class, constructor_args, properties)
            java_file.write(java_method + "\n")
        
        java_file.write("}\n")

if __name__ == "__main__":
    xml_input_file = "application-context.xml"
    java_output_file = "AppConfig.java"
    convert_xml_to_java_config(xml_input_file, java_output_file)
    print(f"Java configuration has been written to {java_output_file}")
