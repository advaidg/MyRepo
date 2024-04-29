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
