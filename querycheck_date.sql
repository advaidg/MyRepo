WITH DateRange AS (
  SELECT TRUNC(DATE '2022-01-01') + LEVEL - 1 AS DateGenerated
  FROM dual
  CONNECT BY TRUNC(DATE '2022-01-01') + LEVEL - 1 <= TRUNC(DATE '2025-12-31')
)
SELECT d.DateGenerated
FROM DateRange d
LEFT JOIN your_table_name t ON d.DateGenerated = TRUNC(t.load_date)
WHERE t.load_date IS NULL
ORDER BY d.DateGenerated;
