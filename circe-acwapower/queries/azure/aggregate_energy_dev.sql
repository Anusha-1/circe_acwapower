-- last_rolling_period source

WITH MaxTimestamps AS (
    SELECT 
        MAX(timestamp) AS max_timestamp
    FROM [vis].[oper_10min]
),
AggregatedData AS (
    SELECT 
        id_wtg,
        id_wf,
        timestamp,
        power,
        CASE 
            WHEN timestamp >= DATEADD(hour, -24, max_timestamp) THEN power ELSE 0 
        END AS power_24h,
        CASE 
            WHEN timestamp >= DATEADD(year,-1,DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)) THEN power ELSE 0 
        END AS power_mtd,
        CASE 
            WHEN timestamp >= DATEADD(year,-1,DATEFROMPARTS(YEAR(GETDATE()), 1, 1)) THEN power ELSE 0 
        END AS power_ytd
    FROM [vis].[oper_10min], MaxTimestamps
)
SELECT 
    id_wtg,
    id_wf,
    SUM(power_24h)/6 AS energy_24h,
    SUM(power_mtd)/6 AS energy_mtd,
    SUM(power_ytd)/6 AS energy_ytd
FROM AggregatedData
GROUP BY id_wtg, id_wf;
