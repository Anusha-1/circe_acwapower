CREATE VIEW "intermediate.10min_horizons" AS
SELECT id_wtg_complete, DATETIME(MAX(timestamp), '-15 minutes') as horizon_datetime
FROM "vis.oper_10min" om 
GROUP BY id_wtg_complete;
