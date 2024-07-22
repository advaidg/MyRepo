import org.w3c.dom.*;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.*;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.util.*;

public class XMLComparator {

    public static void removeElements(Node node, List<String> tagsToRemove) {
        if (node.getNodeType() == Node.ELEMENT_NODE) {
            Element element = (Element) node;
            List<Node> nodesToRemove = new ArrayList<>();
            for (String tag : tagsToRemove) {
                NodeList children = element.getElementsByTagName(tag);
                for (int i = 0; i < children.getLength(); i++) {
                    nodesToRemove.add(children.item(i));
                }
            }
            for (Node child : nodesToRemove) {
                element.removeChild(child);
            }
            NodeList children = element.getChildNodes();
            for (int i = 0; i < children.getLength(); i++) {
                removeElements(children.item(i), tagsToRemove);
            }
        }
    }

    public static void normalizeXML(Node node) {
        if (node.getNodeType() == Node.ELEMENT_NODE) {
            Element element = (Element) node;
            List<Element> children = new ArrayList<>();
            NodeList childNodes = element.getChildNodes();
            for (int i = 0; i < childNodes.getLength(); i++) {
                Node child = childNodes.item(i);
                if (child.getNodeType() == Node.ELEMENT_NODE) {
                    children.add((Element) child);
                }
            }

            // Normalize each child element
            for (Element child : children) {
                normalizeXML(child);
            }

            // Sort children based on tag name and text content
            children.sort(Comparator.comparing(e -> e.getTagName() + ":" + e.getTextContent().trim()));

            // Remove and re-add sorted children to ensure consistent order
            for (Element child : children) {
                element.removeChild(child);
            }
            for (Element child : children) {
                element.appendChild(child);
            }
        }
    }

    public static void saveXML(String filePath, Document doc) throws Exception {
        Transformer transformer = TransformerFactory.newInstance().newTransformer();
        transformer.setOutputProperty(OutputKeys.INDENT, "yes");
        transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
        DOMSource source = new DOMSource(doc);
        StreamResult result = new StreamResult(new File(filePath));
        transformer.transform(source, result);
    }

    public static void compareXMLs(String file1, String file2, List<String> tagsToRemove) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc1 = builder.parse(new File(file1));
        Document doc2 = builder.parse(new File(file2));

        // Remove specified elements
        removeElements(doc1.getDocumentElement(), tagsToRemove);
        removeElements(doc2.getDocumentElement(), tagsToRemove);

        // Normalize XML data
        normalizeXML(doc1.getDocumentElement());
        normalizeXML(doc2.getDocumentElement());

        // Save normalized XML files for inspection (optional)
        saveXML("normalized_" + new File(file1).getName(), doc1);
        saveXML("normalized_" + new File(file2).getName(), doc2);

        // Compare XML data
        List<String> differences = new ArrayList<>();
        compareXMLNodes("", doc1.getDocumentElement(), doc2.getDocumentElement(), differences);

        if (differences.isEmpty()) {
            System.out.println("No differences found. The XML files are equivalent after removing specified elements and normalization.");
        } else {
            System.out.println("Differences found:");
            differences.forEach(System.out::println);
        }
    }

    public static void compareXMLNodes(String path, Node node1, Node node2, List<String> differences) {
        if (node1 == null || node2 == null) {
            differences.add("Node is null at " + path + ": " + (node1 == null ? "missing in first XML" : "missing in second XML"));
            return;
        }

        if (node1.getNodeType() == Node.ELEMENT_NODE && node2.getNodeType() == Node.ELEMENT_NODE) {
            Element element1 = (Element) node1;
            Element element2 = (Element) node2;

            if (!element1.getTagName().equals(element2.getTagName())) {
                differences.add("Tag name differs at " + path + ": " + element1.getTagName() + " vs " + element2.getTagName());
                return;
            }

            NodeList children1 = element1.getChildNodes();
            NodeList children2 = element2.getChildNodes();
            List<Node> nodeList1 = new ArrayList<>();
            List<Node> nodeList2 = new ArrayList<>();

            for (int i = 0; i < children1.getLength(); i++) {
                if (children1.item(i).getNodeType() == Node.ELEMENT_NODE) {
                    nodeList1.add(children1.item(i));
                }
            }
            for (int i = 0; i < children2.getLength(); i++) {
                if (children2.item(i).getNodeType() == Node.ELEMENT_NODE) {
                    nodeList2.add(children2.item(i));
                }
            }

            if (nodeList1.size() != nodeList2.size()) {
                differences.add("Number of child elements differs at " + path + ": " + nodeList1.size() + " vs " + nodeList2.size());
                return;
            }

            // Compare each child element
            for (int i = 0; i < nodeList1.size(); i++) {
                compareXMLNodes(path + "/" + nodeList1.get(i).getNodeName() + "[" + i + "]", nodeList1.get(i), nodeList2.get(i), differences);
            }
        } else if (!node1.getNodeName().equals(node2.getNodeName())) {
            differences.add("Node name differs at " + path + ": " + node1.getNodeName() + " vs " + node2.getNodeName());
        }
    }

    public static void main(String[] args) {
        String file1 = "file1.xml"; // Replace with your XML file path
        String file2 = "file2.xml"; // Replace with your XML file path
        List<String> tagsToRemove = List.of("timestamp", "id"); // Replace with tags to remove before comparison

        try {
            compareXMLs(file1, file2, tagsToRemove);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
