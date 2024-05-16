WITH date_series AS (
  SELECT TRUNC((SELECT MIN(load_dt) FROM your_table)) + LEVEL - 1 AS dt
  FROM dual
  CONNECT BY TRUNC((SELECT MIN(load_dt) FROM your_table)) + LEVEL - 1 <= TRUNC(SYSDATE)
)
SELECT ds.dt AS missing_date
FROM date_series ds
LEFT JOIN your_table yt ON ds.dt = TRUNC(yt.load_dt)
WHERE yt.load_dt IS NULL;
