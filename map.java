public class CustomMapJdbcItemWriter implements ItemWriter<Map<String, String>> {

    private final NamedParameterJdbcTemplate namedParameterJdbcTemplate;

    @Autowired
    public CustomMapJdbcItemWriter(NamedParameterJdbcTemplate namedParameterJdbcTemplate) {
        this.namedParameterJdbcTemplate = namedParameterJdbcTemplate;
    }

    @Override
    public void write(List<? extends Map<String, String>> items) throws Exception {
        String sql = "insert into person (id, name, constant1, constant2) values (:id, :name, :constant1, :constant2)";

        SqlParameterSource[] batchParams = SqlParameterSourceUtils.createBatch(items.toArray());

        // Execute the batch update
        namedParameterJdbcTemplate.batchUpdate(sql, batchParams);
    }
}
