-- last_rolling_period source

CREATE VIEW "last_rolling_period" AS 
SELECT id_wtg_complete, timestamp, wind_speed, power,
		'last rolling month' AS period
FROM "vis.oper_10min" vom
WHERE timestamp >= date((SELECT MAX(timestamp) FROM "vis.oper_10min"), '-30 days')

UNION ALL

SELECT id_wtg_complete, timestamp, wind_speed, power,
		'last rolling year' AS period
FROM "vis.oper_10min" vom
WHERE timestamp >= date((SELECT MAX(timestamp) FROM "vis.oper_10min"), '-365 days');
