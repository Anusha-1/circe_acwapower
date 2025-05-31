-- "vis.power_curves_periods" source

CREATE VIEW "vis.power_curves_periods" AS
SELECT
    id_wtg_complete,
    sector_name,
    wind_speed,
    power,
    period,
    concept,
    density,
    True as reference
FROM
    "vis.interpolated_power_curves"
WHERE
    period IN ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
UNION
SELECT
    id_wtg_complete,
    sector_name,
    wind_speed_corrected as wind_speed,
    power,
    '15 days' AS period,
    '10min data' AS concept,
    density_corrected as density,
    False as reference
FROM(
    SELECT iwsc.*, ibm.power, ibm.sector_name 
	FROM "intermediate.wind_speed_corrections" iwsc 
	JOIN "intermediate.basic_10min" ibm  ON ibm."timestamp" = iwsc."timestamp" AND ibm.id_wtg_complete = iwsc.id_wtg_complete)
WHERE
    timestamp >= datetime('now', '-15 days')
ORDER BY 
	reference ASC,
	concept ASC,
    period ASC,
	id_wtg_complete ASC,
	wind_speed ASC;