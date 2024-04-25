DECLARE
  TYPE TableList IS TABLE OF VARCHAR2(50);
  tables TableList := TableList('table1', 'table2', 'table3');
  v_count NUMBER;
BEGIN
  FOR i IN 1 .. tables.COUNT LOOP
    EXECUTE IMMEDIATE 'SELECT COUNT(*) FROM ' || tables(i) || ' WHERE status = ''Active''' INTO v_count;
    DBMS_OUTPUT.PUT_LINE('Count of active records in ' || tables(i) || ': ' || TO_CHAR(v_count));
  END LOOP;
END;
/
