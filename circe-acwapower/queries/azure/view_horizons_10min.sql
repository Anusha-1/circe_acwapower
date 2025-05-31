CREATE VIEW [intermediate].[10min_horizons] AS
SELECT id_wtg_complete, DATEADD(MINUTE, -15, MAX(timestamp)) as horizon_datetime
FROM vis.oper_10min om 
GROUP BY id_wtg_complete;