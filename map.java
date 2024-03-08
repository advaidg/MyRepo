public class MapEntryJdbcWriter implements ItemWriter<Map<String, String>> {

    private final NamedParameterJdbcTemplate jdbcTemplate;

    public MapEntryJdbcWriter(NamedParameterJdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public void write(List<? extends Map<String, String>> items) throws Exception {
        for (Map<String, String> entry : items) {
            String column1Value = entry.get("yourKey1"); // Replace with the actual key
            String column2Value = entry.get("yourKey2"); // Replace with the actual key

            // Assuming 'your_table' is the name of your table
            String sql = "INSERT INTO your_table (column1, column2) VALUES (:column1, :column2)";

            Map<String, Object> parameters = Map.of("column1", column1Value, "column2", column2Value);

            jdbcTemplate.update(sql, parameters);
        }
    }
}
