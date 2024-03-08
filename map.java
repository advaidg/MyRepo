    public JdbcBatchItemWriter<Map<String, String>> jdbcBatchItemWriter() {
        JdbcBatchItemWriter<Map<String, String>> writer = new JdbcBatchItemWriter<>();
        writer.setDataSource(dataSource);
        writer.setSql("INSERT INTO your_table_name (column1, column2) VALUES (?, ?)");
        writer.setItemPreparedStatementSetter((item, preparedStatement) -> {
            preparedStatement.setString(1, item.getKey());
            preparedStatement.setString(2, item.getValue());
        });
        writer.setAssertUpdates(false); // Disable update count checks for better performance
        writer.setItemSqlParameterSourceProvider(new MapSqlParameterSourceProvider()); // Optional, helps with named parameters

        // Set the batch size for optimal performance
        writer.setPageSize(BATCH_SIZE);
        return writer;
    }
