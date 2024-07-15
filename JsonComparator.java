import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.flipkart.zjsonpatch.JsonDiff;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Comparator;
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

    public static JsonNode sortJson(JsonNode node, String sortKey) {
        if (node.isObject()) {
            ObjectNode sortedNode = new ObjectMapper().createObjectNode();
            node.fieldNames().forEachRemaining(field -> sortedNode.set(field, sortJson(node.get(field), sortKey)));
            return sortedNode;
        } else if (node.isArray()) {
            ArrayNode sortedArray = new ObjectMapper().createArrayNode();
            List<JsonNode> nodeList = new ArrayList<>();
            node.forEach(nodeList::add);

            if (sortKey != null && nodeList.stream().allMatch(n -> n.has(sortKey))) {
                nodeList.sort(Comparator.comparing(n -> n.get(sortKey).asText()));
            } else {
                nodeList.sort(Comparator.comparing(JsonNode::toString));
            }
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

    public static void compareJsons(String file1, String file2, List<String> keysToRemove, String sortKey) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode json1 = mapper.readTree(new File(file1));
        JsonNode json2 = mapper.readTree(new File(file2));

        // Remove specified elements
        removeElements(json1, keysToRemove);
        removeElements(json2, keysToRemove);

        // Sort JSON data
        JsonNode sortedJson1 = sortJson(json1, sortKey);
        JsonNode sortedJson2 = sortJson(json2, sortKey);

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
                JsonNode value = d.get("value");
                if ("replace".equals(op) || "add".equals(op) || "remove".equals(op)) {
                    System.out.println(op.toUpperCase() + " " + value + " at " + path);
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
        String sortKey = "unique_id"; // Replace with the unique key for sorting lists of dictionaries, if applicable

        try {
            compareJsons(file1, file2, keysToRemove, sortKey);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
