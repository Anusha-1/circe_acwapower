-- intermediate.power_curves_periods_timestamps source

CREATE VIEW "intermediate.power_curves_periods_timestamps" AS
SELECT
	datetime('now') as timestamp, 
    id_wtg_complete,
    sector_name,
    wind_speed,
    power,
    period,
    concept,
    density,
    CAST(1 AS BIT) AS reference
FROM
    "vis.interpolated_power_curves"
WHERE
    concept IN ('Historical', 'Monthly', 'Recent')
UNION
SELECT
	timestamp,
    id_wtg_complete,
    sector_name,
    wind_speed_corrected as wind_speed,
    power,
    '15 days' AS period,
    '10min data' AS concept,
    density_corrected as density,
    CAST(0 AS BIT) AS reference
FROM
    (
    SELECT iwsc.*, ibm.power, ibm.sector_name 
    FROM "intermediate.wind_speed_corrections" iwsc 
    JOIN "intermediate.basic_10min" ibm 
        ON ibm."timestamp" = iwsc."timestamp" 
        AND ibm.id_wtg_complete = iwsc.id_wtg_complete
    ) AS subquery_alias;