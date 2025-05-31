CREATE VIEW "intermediate.10min_horizons_basic" AS
SELECT id_wtg_complete, DATETIME(MAX(timestamp), '-15 minutes') as horizon_datetime
FROM "intermediate.basic_10min" om 
GROUP BY id_wtg_complete;
