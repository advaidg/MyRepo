import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class JsonComparator {

    public static void removeElements(JsonNode node, List<String> keysToRemove) {
        if (node.isObject()) {
            ObjectNode objNode = (ObjectNode) node;
            for (String key : keysToRemove) {
                objNode.remove(key);
            }
            Iterator<JsonNode> elements = objNode.elements();
            while (elements.hasNext()) {
                removeElements(elements.next(), keysToRemove);
            }
        } else if (node.isArray()) {
            ArrayNode arrNode = (ArrayNode) node;
            for (JsonNode item : arrNode) {
                removeElements(item, keysToRemove);
            }
        }
    }

    public static JsonNode normalizeJson(JsonNode node) {
        if (node.isObject()) {
            ObjectNode sortedNode = new ObjectMapper().createObjectNode();
            List<String> fieldNames = new ArrayList<>();
            node.fieldNames().forEachRemaining(fieldNames::add);
            Collections.sort(fieldNames);
            for (String fieldName : fieldNames) {
                sortedNode.set(fieldName, normalizeJson(node.get(fieldName)));
            }
            return sortedNode;
        } else if (node.isArray()) {
            ArrayNode sortedArray = new ObjectMapper().createArrayNode();
            List<JsonNode> nodeList = new ArrayList<>();
            node.forEach(nodeList::add);
            nodeList.sort(Comparator.comparing(JsonNode::toString));
            nodeList.forEach(sortedArray::add);
            return sortedArray;
        } else {
            return node;
        }
    }

    public static void saveJson(String filePath, JsonNode data) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), data);
    }

    public static void compareJsons(String file1, String file2, List<String> keysToRemove) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode json1 = mapper.readTree(new File(file1));
        JsonNode json2 = mapper.readTree(new File(file2));

        // Remove specified elements
        removeElements(json1, keysToRemove);
        removeElements(json2, keysToRemove);

        // Normalize JSON data
        JsonNode normalizedJson1 = normalizeJson(json1);
        JsonNode normalizedJson2 = normalizeJson(json2);

        // Save modified and normalized JSON files for inspection (optional)
        saveJson("normalized_" + file1, normalizedJson1);
        saveJson("normalized_" + file2, normalizedJson2);

        // Compare JSON data
        List<String> differences = new ArrayList<>();
        compareJsonNodes("", normalizedJson1, normalizedJson2, differences);

        if (differences.isEmpty()) {
            System.out.println("No differences found. The JSON files are equivalent after removing specified elements and normalization.");
        } else {
            System.out.println("Differences found:");
            differences.forEach(System.out::println);
        }
    }

    public static void compareJsonNodes(String path, JsonNode node1, JsonNode node2, List<String> differences) {
        if (node1 == null || node2 == null) {
            differences.add("Node missing at " + path + ": " + (node1 == null ? "missing in first JSON" : "missing in second JSON"));
            return;
        }

        if (node1.isObject() && node2.isObject()) {
            Set<String> fieldNames = new HashSet<>();
            node1.fieldNames().forEachRemaining(fieldNames::add);
            node2.fieldNames().forEachRemaining(fieldNames::add);

            for (String fieldName : fieldNames) {
                JsonNode field1 = node1.get(fieldName);
                JsonNode field2 = node2.get(fieldName);
                compareJsonNodes(path + "/" + fieldName, field1, field2, differences);
            }
        } else if (node1.isArray() && node2.isArray()) {
            if (node1.size() != node2.size()) {
                differences.add("Array size differs at " + path + ": " + node1.size() + " vs " + node2.size());
            } else {
                for (int i = 0; i < node1.size(); i++) {
                    compareJsonNodes(path + "[" + i + "]", node1.get(i), node2.get(i), differences);
                }
            }
        } else if (!node1.equals(node2)) {
            differences.add("Value differs at " + path + ": " + node1 + " vs " + node2);
        }
    }

    public static void main(String[] args) {
        String file1 = "file1.json"; // Replace with your JSON file path
        String file2 = "file2.json"; // Replace with your JSON file path
        List<String> keysToRemove = List.of("timestamp", "id"); // Replace with keys to remove before comparison

        try {
            compareJsons(file1, file2, keysToRemove);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
