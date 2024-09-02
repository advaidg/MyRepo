import xml.etree.ElementTree as ET

def convert_xml_to_java_config(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(output_file, "w") as java_file:
        java_file.write("import org.springframework.context.annotation.Bean;\n")
        java_file.write("import org.springframework.context.annotation.Configuration;\n")
        java_file.write("import org.springframework.orm.jpa.support.SharedEntityManagerBean;\n")
        java_file.write("import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;\n")
        java_file.write("import org.springframework.orm.jpa.vendor.HibernateJpaVendorAdapter;\n")
        java_file.write("import javax.sql.DataSource;\n\n")

        java_file.write("@Configuration\n")
        java_file.write("public class AppConfig {\n\n")

        for bean in root.findall("bean"):
            bean_id = bean.get("id")
            bean_class = bean.get("class")

            if bean_class == "org.springframework.orm.jpa.support.SharedEntityManagerBean":
                java_file.write(f"    @Bean\n")
                java_file.write(f"    public {bean_class} {bean_id}() {{\n")
                java_file.write(f"        SharedEntityManagerBean bean = new SharedEntityManagerBean();\n")
                for prop in bean.findall("property"):
                    ref = prop.get("ref")
                    java_file.write(f"        bean.setEntityManagerFactory({ref}().getObject());\n")
                java_file.write(f"        return bean;\n")
                java_file.write(f"    }}\n\n")

            elif bean_class == "org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean":
                java_file.write(f"    @Bean\n")
                java_file.write(f"    public {bean_class} {bean_id}() {{\n")
                java_file.write(f"        LocalContainerEntityManagerFactoryBean bean = new LocalContainerEntityManagerFactoryBean();\n")
                for prop in bean.findall("property"):
                    name = prop.get("name")
                    value = prop.get("value")
                    ref = prop.get("ref")
                    nested_bean = prop.find("bean")

                    if value:
                        java_file.write(f"        bean.set{name.capitalize()}(\"{value}\");\n")
                    elif ref:
                        java_file.write(f"        bean.set{name.capitalize()}({ref}());\n")
                    elif nested_bean is not None:
                        nested_class = nested_bean.get("class")
                        java_file.write(f"        bean.set{name.capitalize()}(new {nested_class}());\n")
                java_file.write(f"        return bean;\n")
                java_file.write(f"    }}\n\n")

        java_file.write("    // Define your DataSource bean here\n")
        java_file.write("    @Bean\n")
        java_file.write("    public DataSource applicationDatasource() {\n")
        java_file.write("        // Configure and return the appropriate DataSource\n")
        java_file.write("        return new YourDataSourceImplementation();\n")
        java_file.write("    }\n\n")

        java_file.write("}\n")

if __name__ == "__main__":
    xml_input_file = "application-context.xml"  # Replace with your file path if needed
    java_output_file = "AppConfig.java"
    convert_xml_to_java_config(xml_input_file, java_output_file)
    print(f"Java configuration has been written to {java_output_file}")
