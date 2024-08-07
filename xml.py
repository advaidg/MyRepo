import os
from lxml import etree

class WebXmlParser:
    def __init__(self, input_file, output_dir, config_class_name="WebConfig"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.config_class_name = config_class_name
        self.config_content = ""

    def parse_web_xml(self):
        tree = etree.parse(self.input_file)
        root = tree.getroot()
        ns = {"ns": "http://java.sun.com/xml/ns/javaee"}

        self.parse_context_params(root, ns)
        self.parse_filters(root, ns)
        self.parse_filter_mappings(root, ns)
        self.parse_servlets(root, ns)
        self.parse_servlet_mappings(root, ns)
        self.parse_listeners(root, ns)
        self.parse_error_pages(root, ns)

        self.generate_combined_config_class()

    def parse_context_params(self, root, ns):
        context_params = root.findall("ns:context-param", ns)
        for param in context_params:
            param_name = param.find("ns:param-name", ns).text
            param_value = param.find("ns:param-value", ns).text
            self.add_context_param_config(param_name, param_value)

    def parse_filters(self, root, ns):
        filters = root.findall("ns:filter", ns)
        for filter_element in filters:
            filter_name = filter_element.find("ns:filter-name", ns).text
            filter_class = filter_element.find("ns:filter-class", ns).text
            self.add_filter_config(filter_name, filter_class)

    def parse_filter_mappings(self, root, ns):
        filter_mappings = root.findall("ns:filter-mapping", ns)
        for mapping in filter_mappings:
            filter_name = mapping.find("ns:filter-name", ns).text
            url_pattern = mapping.find("ns:url-pattern", ns).text
            self.add_filter_mapping_config(filter_name, url_pattern)

    def parse_servlets(self, root, ns):
        servlets = root.findall("ns:servlet", ns)
        for servlet in servlets:
            servlet_name = servlet.find("ns:servlet-name", ns).text
            servlet_class = servlet.find("ns:servlet-class", ns).text
            self.add_servlet_config(servlet_name, servlet_class)

    def parse_servlet_mappings(self, root, ns):
        servlet_mappings = root.findall("ns:servlet-mapping", ns)
        for mapping in servlet_mappings:
            servlet_name = mapping.find("ns:servlet-name", ns).text
            url_pattern = mapping.find("ns:url-pattern", ns).text
            self.add_servlet_mapping_config(servlet_name, url_pattern)

    def parse_listeners(self, root, ns):
        listeners = root.findall("ns:listener", ns)
        for listener in listeners:
            listener_class = listener.find("ns:listener-class", ns).text
            self.add_listener_config(listener_class)

    def parse_error_pages(self, root, ns):
        error_pages = root.findall("ns:error-page", ns)
        for error_page in error_pages:
            location = error_page.find("ns:location", ns).text
            error_code = error_page.find("ns:error-code", ns)
            exception_type = error_page.find("ns:exception-type", ns)

            if error_code is not None:
                error_code = error_code.text
                self.add_error_page_config(error_code, location, is_exception=False)
            elif exception_type is not None:
                exception_type = exception_type.text
                self.add_error_page_config(exception_type, location, is_exception=True)

    def add_context_param_config(self, param_name, param_value):
        bean_definition = f"""    @Bean
    public String {param_name}() {{
        return "{param_value}";
    }}\n\n"""
        self.config_content += bean_definition

    def add_filter_config(self, filter_name, filter_class):
        bean_definition = f"""    @Bean
    public FilterRegistrationBean<{filter_class.split('.')[-1]}> {filter_name}() {{
        FilterRegistrationBean<{filter_class.split('.')[-1]}> registrationBean = 
            new FilterRegistrationBean<>(new {filter_class.split('.')[-1]}());
        registrationBean.addUrlPatterns("/*");
        return registrationBean;
    }}\n\n"""
        self.config_content += bean_definition

    def add_filter_mapping_config(self, filter_name, url_pattern):
        bean_definition = f"""    @Bean
    public FilterRegistrationBean<?> {filter_name}Mapping() {{
        FilterRegistrationBean<?> registrationBean = new FilterRegistrationBean<>();
        registrationBean.setFilter(new {filter_name}());
        registrationBean.addUrlPatterns("{url_pattern}");
        return registrationBean;
    }}\n\n"""
        self.config_content += bean_definition

    def add_servlet_config(self, servlet_name, servlet_class):
        bean_definition = f"""    @Bean
    public ServletRegistrationBean<{servlet_class.split('.')[-1]}> {servlet_name}() {{
        ServletRegistrationBean<{servlet_class.split('.')[-1]}> registrationBean = 
            new ServletRegistrationBean<>(new {servlet_class.split('.')[-1]}(), "/*");
        return registrationBean;
    }}\n\n"""
        self.config_content += bean_definition

    def add_servlet_mapping_config(self, servlet_name, url_pattern):
        bean_definition = f"""    @Bean
    public ServletRegistrationBean<?> {servlet_name}Mapping() {{
        ServletRegistrationBean<?> registrationBean = new ServletRegistrationBean<>();
        registrationBean.setServlet(new {servlet_name}());
        registrationBean.addUrlPatterns("{url_pattern}");
        return registrationBean;
    }}\n\n"""
        self.config_content += bean_definition

    def add_listener_config(self, listener_class):
        bean_definition = f"""    @Bean
    public ServletListenerRegistrationBean<{listener_class.split('.')[-1]}> {listener_class.split('.')[-1]}Listener() {{
        return new ServletListenerRegistrationBean<>(new {listener_class.split('.')[-1]}());
    }}\n\n"""
        self.config_content += bean_definition

    def add_error_page_config(self, error_or_exception, location, is_exception):
        error_type = "Exception" if is_exception else "Error"
        bean_definition = f"""    @Bean
    public ErrorPageRegistrar errorPageRegistrar() {{
        return new ErrorPageRegistrar() {{
            @Override
            public void registerErrorPages(ErrorPageRegistry registry) {{
                registry.addErrorPages(new ErrorPage({error_or_exception}.class, "{location}"));
            }}
        }};
    }}\n\n"""
        self.config_content += bean_definition

    def generate_combined_config_class(self):
        content = f"""import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.boot.web.servlet.ServletListenerRegistrationBean;
import org.springframework.boot.web.servlet.error.ErrorPageRegistrar;
import org.springframework.boot.web.servlet.error.ErrorPageRegistry;
import org.springframework.boot.web.servlet.error.ErrorPage;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class {self.config_class_name} {{

{self.config_content}}}
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
    input_file = "path/to/web.xml"
    output_dir = "path/to/output"
    parser = WebXmlParser(input_file, output_dir)
    parser.parse_web_xml()
