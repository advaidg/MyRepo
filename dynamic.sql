DECLARE
  -- Cursor to select tables that contain the specific column
  CURSOR table_cur IS
    SELECT table_name
    FROM all_tab_columns
    WHERE column_name = 'YOUR_COLUMN_NAME' AND owner = 'YOUR_SCHEMA';

  -- Variable to build and execute dynamic SQL
  v_sql VARCHAR2(1000);
  v_count NUMBER;
BEGIN
  FOR rec IN table_cur LOOP
    -- Construct SQL to check for the specific value
    v_sql := 'SELECT COUNT(*) FROM ' || rec.table_name || 
             ' WHERE YOUR_COLUMN_NAME LIKE ''%;123;%''';

    EXECUTE IMMEDIATE v_sql INTO v_count;

    -- Output results if rows are found
    IF v_count > 0 THEN
      dbms_output.put_line('Table ' || rec.table_name || ' has rows with the value ;123;');
    END IF;
  END LOOP;
END;
