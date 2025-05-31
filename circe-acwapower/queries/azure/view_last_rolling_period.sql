-- vis.last_rolling_period source


CREATE VIEW vis.last_rolling_period AS
SELECT id_wtg_complete, timestamp, wind_speed, power,
		'last_rolling_month' AS period
FROM vis.oper_10min om 
WHERE timestamp >= DATEADD(day,-30,(SELECT MAX(timestamp) FROM vis.oper_10min om))

UNION ALL

SELECT id_wtg_complete, timestamp, wind_speed, power,
		'last_rolling_year' AS period
FROM vis.oper_10min om 
WHERE timestamp >= DATEADD(day,-365,(SELECT MAX(timestamp) FROM vis.oper_10min om));