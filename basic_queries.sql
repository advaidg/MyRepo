1. Database Instance Information
This query gives you basic information about the database instance, including the version, status, and uptime:

sql
Copy code
SELECT instance_name, version, status, startup_time FROM v$instance;
2. System and User Load
This query shows the number of active sessions and can give a quick overview of the current load on the database:

sql
Copy code
SELECT username, status, COUNT(*) AS session_count 
FROM v$session 
GROUP BY username, status;
3. Tablespaces and Disk Usage
It's crucial to ensure that you have enough free space in your tablespaces to prevent issues:

sql
Copy code
SELECT tablespace_name, file_name, bytes / 1024 / 1024 AS size_MB,
       maxbytes / 1024 / 1024 AS max_size_MB, autoextensible 
FROM dba_data_files
ORDER BY tablespace_name;
4. Performance Metrics
Check for any unusual wait events or bottlenecks:

sql
Copy code
SELECT event, total_waits, time_waited, average_wait 
FROM v$system_event 
WHERE wait_class <> 'Idle'
ORDER BY time_waited DESC;
5. Database Locks
Locks can often cause performance issues, so it's useful to check for any session that is holding locks:

sql
Copy code
SELECT sid, username, osuser, object_id, object_name, locktype, mode_held
FROM v$locked_object lo
JOIN dba_objects do ON lo.object_id = do.object_id
JOIN v$lock l ON lo.object_id = l.id1
JOIN v$session s ON lo.session_id = s.sid;
6. Alert Log Entries
Reviewing the alert log can help you identify any critical errors or warnings:

sql
Copy code
-- This query assumes you're using Oracle 12c or newer, where X$DBGALERTEXT is available.
SELECT originating_timestamp, message_text
FROM x$dbgalertext
WHERE originating_timestamp > SYSDATE - 1
ORDER BY originating_timestamp DESC;
7. Automatic Workload Repository (AWR) Snapshots
AWR snapshots provide a wide range of performance data:

sql
Copy code
SELECT * FROM dba_hist_snapshot ORDER BY snap_id DESC;
