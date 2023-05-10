   List<Object> parameterValues = Arrays.asList(1, prd.toArray());

    // Set the parameter values using PreparedStatementSetter
    reader.setPreparedStatementSetter(new PreparedStatementSetter() {
        public void setValues(PreparedStatement ps) throws SQLException {
            // Set the parameter values using PreparedStatement
            ps.setObject(1, parameterValues.get(0));
            for (int i = 0; i < prd.size(); i++) {
                ps.setObject(i + 2, parameterValues.get(i + 1));
            }
        }
    });
