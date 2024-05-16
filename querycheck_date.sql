WITH DateRange AS (
  SELECT TRUNC(TO_DATE('2022-01-01', 'YYYY-MM-DD')) + LEVEL - 1 AS DateGenerated
  FROM dual
  CONNECT BY TRUNC(TO_DATE('2022-01-01', 'YYYY-MM-DD')) + LEVEL - 1 <= TRUNC(SYSDATE)
)
SELECT d.DateGenerated
FROM DateRange d
LEFT JOIN your_table_name t ON d.DateGenerated = t.load_date
WHERE t.load_date IS NULL
ORDER BY d.DateGenerated;
