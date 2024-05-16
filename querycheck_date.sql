WITH DateRange AS (
  SELECT DATE '2022-01-01' + LEVEL - 1 AS DateGenerated
  FROM dual
  CONNECT BY DATE '2022-01-01' + LEVEL - 1 <= DATE '2025-12-31'
)
SELECT d.DateGenerated
FROM DateRange d
LEFT JOIN your_table_name t ON d.DateGenerated = TRUNC(t.load_date)
WHERE t.load_date IS NULL
ORDER BY d.DateGenerated;
