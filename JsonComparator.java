import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.flipkart.zjsonpatch.JsonDiff;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Iterator;
import java.util.List;

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

    public static JsonNode sortJson(JsonNode node) {
        if (node.isObject()) {
            ObjectNode sortedNode = new ObjectMapper().createObjectNode();
            node.fieldNames().asIterator().forEachRemaining(field -> sortedNode.set(field, sortJson(node.get(field))));
            List<String> sortedKeys = new ArrayList<>();
            node.fieldNames().forEachRemaining(sortedKeys::add);
            Collections.sort(sortedKeys);
            ObjectNode sortedObjNode = new ObjectMapper().createObjectNode();
            for (String key : sortedKeys) {
                sortedObjNode.set(key, sortedNode.get(key));
            }
            return sortedObjNode;
        } else if (node.isArray()) {
            ArrayNode sortedArray = new ObjectMapper().createArrayNode();
            List<JsonNode> nodeList = new ArrayList<>();
            node.forEach(nodeList::add);
            nodeList.sort((a, b) -> a.toString().compareTo(b.toString()));
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

        // Sort JSON data
        JsonNode sortedJson1 = sortJson(json1);
        JsonNode sortedJson2 = sortJson(json2);

        // Save modified and sorted JSON files for inspection (optional)
        saveJson("sorted_" + file1, sortedJson1);
        saveJson("sorted_" + file2, sortedJson2);

        // Compare JSON data
        JsonNode diff = JsonDiff.asJson(sortedJson1, sortedJson2);

        // Print readable summary of differences
        if (diff.size() > 0) {
            System.out.println("Differences found:");
            for (JsonNode d : diff) {
                String op = d.get("op").asText();
                String path = d.get("path").asText();
                switch (op) {
                    case "add":
                        System.out.println("Added value: " + d.get("value") + " at " + path);
                        break;
                    case "remove":
                        JsonNode removedValue = sortedJson1.at(path);
                        System.out.println("Removed value: " + removedValue + " from " + path);
                        break;
                    case "replace":
                        JsonNode oldValue = sortedJson1.at(path);
                        JsonNode newValue = d.get("value");
                        System.out.println("Replaced value: " + oldValue + " with " + newValue + " at " + path);
                        break;
                    default:
                        System.out.println("Unknown operation " + op + " at " + path);
                        break;
                }
            }
        } else {
            System.out.println("No differences found. The JSON files are equivalent after removing specified elements and sorting.");
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
