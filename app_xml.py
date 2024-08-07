import os
from lxml import etree

class SpringXmlParser:
    def __init__(self, input_file, output_dir, config_class_name="ApplicationConfig"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.config_class_name = config_class_name
        self.beans_content = ""

    def parse_spring_xml(self):
        tree = etree.parse(self.input_file)
        root = tree.getroot()
        ns = {"ns": "http://www.springframework.org/schema/beans"}

        self.parse_beans(root, ns)
        self.generate_combined_config_class()

    def parse_beans(self, root, ns):
        beans = root.findall("ns:bean", ns)
        for bean in beans:
            bean_id = bean.get("id")
            bean_class = bean.get("class")
            properties = bean.findall("ns:property", ns)
            constructor_args = bean.findall("ns:constructor-arg", ns)
            self.add_bean_config(bean_id, bean_class, properties, constructor_args)

    def add_bean_config(self, bean_id, bean_class, properties, constructor_args):
        bean_class_name = bean_class.split('.')[-1]

        property_injections = "\n".join(
            [f'        {bean_class_name.lower()}.set{prop.get("name").capitalize()}("{prop.find("ns:value", ns).text}");'
             for prop in properties]
        )

        constructor_injections = ", ".join(
            [f'"{arg.find("ns:value", ns).text}"' for arg in constructor_args]
        )

        if constructor_args:
            bean_definition = f"""    @Bean
    public {bean_class_name} {bean_id}() {{
        {bean_class_name} {bean_class_name.lower()} = new {bean_class_name}({constructor_injections});
{property_injections}
        return {bean_class_name.lower()};
    }}\n\n"""
        else:
            bean_definition = f"""    @Bean
    public {bean_class_name} {bean_id}() {{
        {bean_class_name} {bean_class_name.lower()} = new {bean_class_name}();
{property_injections}
        return {bean_class_name.lower()};
    }}\n\n"""

        self.beans_content += bean_definition

    def generate_combined_config_class(self):
        content = f"""import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class {self.config_class_name} {{

{self.beans_content}}}
"""
        self.write_to_file(self.config_class_name, content)

    def write_to_file(self, class_name, content):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        file_path = os.path.join(self.output_dir, f"{class_name}.java")
        with open(file_path, "w") as file:
            file.write(content)
        print(f"Generated {file_path}")

if __name__ == "__main__":
    input_file = "path/to/applicationContext.xml"
    output_dir = "path/to/output"
    parser = SpringXmlParser(input_file, output_dir)
    parser.parse_spring_xml()
