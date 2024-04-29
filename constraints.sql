SELECT a.table_name,
       a.constraint_name,
       a.column_name,
       c.table_name as referenced_table,
       c.column_name as referenced_column
FROM all_cons_columns a
JOIN all_constraints b ON a.owner = b.owner AND a.constraint_name = b.constraint_name
JOIN all_cons_columns c ON b.r_owner = c.owner AND b.r_constraint_name = c.constraint_name
WHERE b.constraint_type = 'R'
  AND a.owner = :your_schema_name;  -- Replace :your_schema_name with your actual schema name


SELECT a.table_name, 
       a.constraint_name, 
       a.r_constraint_name as referenced_constraint_name,
       c.owner as referenced_owner,
       c.table_name as referenced_table_name
FROM all_constraints a
JOIN all_constraints c ON a.r_constraint_name = c.constraint_name
WHERE a.constraint_type = 'R'
  AND a.owner = :your_schema_name;  -- Replace :your_schema_name with your actual schema name

ELECT t.table_name
FROM all_tables t
LEFT JOIN all_constraints c ON t.table_name = c.table_name AND c.owner = t.owner
                             AND c.constraint_type = 'R'
WHERE t.owner = 'YOUR_SCHEMA_NAME'  -- Replace with your actual schema name
      AND c.constraint_name IS NULL
ORDER BY t.table_name;
