SELECT dt AS missing_date
FROM (
  SELECT TRUNC(MIN(load_dt)) + LEVEL - 1 AS dt
  FROM your_table
  CONNECT BY TRUNC(MIN(load_dt)) + LEVEL - 1 <= TRUNC(SYSDATE)
  GROUP BY TRUNC(MIN(load_dt))
)
LEFT JOIN your_table ON dt = TRUNC(load_dt)
WHERE load_dt IS NULL;
