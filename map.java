public class CustomMapJdbcItemWriter implements ItemWriter<Map<String, String>> {

    private final JdbcTemplate jdbcTemplate;

    @Autowired
    public CustomMapJdbcItemWriter(JdbcTemplate jdbcTemplate) {
        this.jdbcTemplate = jdbcTemplate;
    }

    @Override
    public void write(List<? extends Map<String, String>> items) throws Exception {
        String sql = "insert into person (id, name, constant1, constant2) values (?, ?, ?, ?)";

        for (Map<String, String> item : items) {
            String id = item.get("id");
            String name = item.get("name");
            String constant1 = "your_constant_value_1";
            String constant2 = "your_constant_value_2";

            // Perform custom logic if needed before or after the insert

            // Execute the insert statement
            jdbcTemplate.update(sql, id, name, constant1, constant2);

            // Perform additional custom logic after the insert if needed
        }
    }
}
