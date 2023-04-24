public class MultiThreadedJsonItemReader<T> implements ItemReader<List<T>> {

    private final String filePath;
    private final Class<T> targetType;
    private final ObjectMapper objectMapper;
    private final int batchSize;

    private List<T> buffer;
    private int offset;

    public MultiThreadedJsonItemReader(String filePath, Class<T> targetType, int batchSize) {
        this.filePath = filePath;
        this.targetType = targetType;
        this.objectMapper = new ObjectMapper();
        this.batchSize = batchSize;
    }

    @Override
    public List<T> read() throws Exception {
        if (buffer == null || offset >= buffer.size()) {
            buffer = readBatch();
            offset = 0;
        }
        if (buffer.isEmpty()) {
            return null;
        }
        int end = Math.min(offset + batchSize, buffer.size());
        List<T> batch = buffer.subList(offset, end);
        offset = end;
        return batch;
    }

    private List<T> readBatch() throws Exception {
        List<T> batch = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            JsonNode root = objectMapper.readTree(reader);
            for (JsonNode node : root) {
                T item = objectMapper.treeToValue(node, targetType);
                batch.add(item);
            }
        }
        return batch;
    }
}
