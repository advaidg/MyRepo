WITH DateGenerator AS (
  SELECT TO_DATE('2022-01-01', 'YYYY-MM-DD') + LEVEL - 1 AS GeneratedDate
  FROM dual
  CONNECT BY LEVEL <= SYSDATE - TO_DATE('2022-01-01', 'YYYY-MM-DD') + 1
)
SELECT d.GeneratedDate
FROM DateGenerator d
LEFT JOIN your_table_name t
ON d.GeneratedDate = t.load_date
WHERE t.load_date IS NULL
ORDER BY d.GeneratedDate;
