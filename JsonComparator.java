import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.flipkart.zjsonpatch.JsonDiff;

import java.io.File;
import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

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

    public static boolean areJsonNodesEqual(JsonNode node1, JsonNode node2) {
        if (node1 == null || node2 == null) {
            return node1 == node2;
        }

        if (node1.isObject() && node2.isObject()) {
            Set<String> fieldNames = new HashSet<>();
            node1.fieldNames().forEachRemaining(fieldNames::add);
            node2.fieldNames().forEachRemaining(fieldNames::add);

            for (String fieldName : fieldNames) {
                if (!areJsonNodesEqual(node1.get(fieldName), node2.get(fieldName))) {
                    return false;
                }
            }
            return true;
        } else if (node1.isArray() && node2.isArray()) {
            if (node1.size() != node2.size()) {
                return false;
            }

            for (int i = 0; i < node1.size(); i++) {
                boolean matchFound = false;
                for (int j = 0; j < node2.size(); j++) {
                    if (areJsonNodesEqual(node1.get(i), node2.get(j))) {
                        matchFound = true;
                        break;
                    }
                }
                if (!matchFound) {
                    return false;
                }
            }
            return true;
        } else {
            return node1.equals(node2);
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

        // Save modified JSON files for inspection (optional)
        saveJson("modified_" + file1, json1);
        saveJson("modified_" + file2, json2);

        // Compare JSON data
        if (areJsonNodesEqual(json1, json2)) {
            System.out.println("No differences found. The JSON files are equivalent after removing specified elements.");
        } else {
            System.out.println("Differences found:");
            JsonNode diff = JsonDiff.asJson(json1, json2);
            for (JsonNode d : diff) {
                String op = d.get("op").asText();
                String path = d.get("path").asText();
                JsonNode value = d.get("value");
                switch (op) {
                    case "add":
                        System.out.println("Added value: " + value + " at " + path);
                        break;
                    case "remove":
                        JsonNode removedValue = json1.at(path);
                        System.out.println("Removed value: " + removedValue + " from " + path);
                        break;
                    case "replace":
                        JsonNode oldValue = json1.at(path);
                        JsonNode newValue = value;
                        System.out.println("Replaced value: " + oldValue + " with " + newValue + " at " + path);
                        break;
                    default:
                        System.out.println("Unknown operation " + op + " at " + path);
                        break;
                }
            }
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
