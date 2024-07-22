import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import java.io.File;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class XMLComparator {

    public static void removeElements(Node node, List<String> tagsToRemove) {
        if (node.getNodeType() == Node.ELEMENT_NODE) {
            Element element = (Element) node;
            for (String tag : tagsToRemove) {
                NodeList children = element.getElementsByTagName(tag);
                for (int i = 0; i < children.getLength(); i++) {
                    Node child = children.item(i);
                    element.removeChild(child);
                }
            }
            NodeList children = element.getChildNodes();
            for (int i = 0; i < children.getLength(); i++) {
                removeElements(children.item(i), tagsToRemove);
            }
        }
    }

    public static Node normalizeXML(Node node) {
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

            children.sort(Comparator.comparing(Element::getTagName));

            for (Element child : children) {
                element.removeChild(child);
            }

            for (Element child : children) {
                element.appendChild(normalizeXML(child));
            }
        }
        return node;
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
        Node normalizedXml1 = normalizeXML(doc1.getDocumentElement());
        Node normalizedXml2 = normalizeXML(doc2.getDocumentElement());

        // Save modified and normalized XML files for inspection (optional)
        saveXML("normalized_" + file1, doc1);
        saveXML("normalized_" + file2, doc2);

        // Compare XML data
        List<String> differences = new ArrayList<>();
        compareXMLNodes("", normalizedXml1, normalizedXml2, differences);

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
            if (children1.getLength() != children2.getLength()) {
                differences.add("Child node count differs at " + path + ": " + children1.getLength() + " vs " + children2.getLength());
                return;
            }

            List<Node> nodeList1 = new ArrayList<>();
            List<Node> nodeList2 = new ArrayList<>();
            for (int i = 0; i < children1.getLength(); i++) {
                nodeList1.add(children1.item(i));
            }
            for (int i = 0; i < children2.getLength(); i++) {
                nodeList2.add(children2.item(i));
            }

            nodeList1.sort(Comparator.comparing(Node::getNodeName));
            nodeList2.sort(Comparator.comparing(Node::getNodeName));

            for (int i = 0; i < nodeList1.size(); i++) {
                compareXMLNodes(path + "/" + nodeList1.get(i).getNodeName(), nodeList1.get(i), nodeList2.get(i), differences);
            }
        } else if (!node1.isEqualNode(node2)) {
            differences.add("Value differs at " + path + ": " + node1.getTextContent() + " vs " + node2.getTextContent());
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
