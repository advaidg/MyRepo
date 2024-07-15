import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.flipkart.zjsonpatch.JsonDiff;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class JsonComparator {

    /**
     * Remove specified keys from the JSON object recursively.
     */
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
            for (JsonNode item : node) {
                removeElements(item, keysToRemove);
            }
        }
    }

    /**
     * Flatten the JSON structure.
     */
    public static void flattenJson(JsonNode node, String parentKey, Map<String, JsonNode> flatMap) {
        if (node.isObject()) {
            node.fields().forEachRemaining(entry -> {
                String newKey = parentKey.isEmpty() ? entry.getKey() : parentKey + "." + entry.getKey();
                flattenJson(entry.getValue(), newKey, flatMap);
            });
        } else if (node.isArray()) {
            for (int i = 0; i < node.size(); i++) {
                flattenJson(node.get(i), parentKey + "[" + i + "]", flatMap);
            }
        } else {
            flatMap.put(parentKey, node);
        }
    }

    /**
     * Load JSON data from a file.
     */
    public static JsonNode loadJson(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readTree(new File(filePath));
    }

    /**
     * Save JSON data to a file.
     */
    public static void saveJson(String filePath, JsonNode data) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        mapper.writerWithDefaultPrettyPrinter().writeValue(new File(filePath), data);
    }

    /**
     * Compare two JSON files after removing specified keys and flattening the JSON data.
     */
    public static void compareJsons(String file1, String file2, List<String> keysToRemove) throws IOException {
        // Load JSON files
        JsonNode json1 = loadJson(file1);
        JsonNode json2 = loadJson(file2);

        // Remove specified elements
        removeElements(json1, keysToRemove);
        removeElements(json2, keysToRemove);

        // Flatten JSON data
        Map<String, JsonNode> flatJson1 = new HashMap<>();
        Map<String, JsonNode> flatJson2 = new HashMap<>();
        flattenJson(json1, "", flatJson1);
        flattenJson(json2, "", flatJson2);

        // Compare flattened JSON data
        ObjectMapper mapper = new ObjectMapper();
        JsonNode diff = JsonDiff.asJson(mapper.valueToTree(flatJson1), mapper.valueToTree(flatJson2));

        if (diff.size() > 0) {
            System.out.println("Differences found:");
            System.out.println(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(diff));
        } else {
            System.out.println("No differences found. The JSON files are equivalent after removing specified elements and flattening.");
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
