import xml.etree.ElementTree as ET

def parse_properties(bean_element):
    properties = []
    for prop in bean_element.findall("property"):
        prop_name = prop.get("name")
        value = prop.get("value")
        ref = prop.get("ref")
        nested_bean = prop.find("bean")

        if value:
            properties.append({"name": prop_name, "value": f'"{value}"'})
        elif ref:
            properties.append({"name": prop_name, "value": f"{ref}()"})
        elif nested_bean is not None:
            nested_class = nested_bean.get("class")
            properties.append({"name": prop_name, "value": f"new {nested_class}()"})
    return properties

def generate_java_method(bean_id, bean_class, constructor_args, properties):
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

def convert_xml_to_java_config(xml_file, output_file):
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
            constructor_args = []  # Assuming no constructor args for simplicity
            properties = parse_properties(bean)
            java_method = generate_java_method(bean_id, bean_class, constructor_args, properties)
            java_file.write(java_method + "\n")
        
        java_file.write("}\n")

if __name__ == "__main__":
    xml_input_file = "application-context.xml"
    java_output_file = "AppConfig.java"
    convert_xml_to_java_config(xml_input_file, java_output_file)
    print(f"Java configuration has been written to {java_output_file}")
