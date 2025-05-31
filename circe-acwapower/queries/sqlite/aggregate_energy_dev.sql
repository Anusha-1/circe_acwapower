-- last_rolling_period source

SELECT 
    id_wtg,
    id_wf,  
    SUM(CASE 
        WHEN timestamp >= datetime((SELECT MAX(timestamp) FROM "vis.oper_10min"), '-24 hours') THEN power
        ELSE 0 
    END)/6 AS energy_24h,
    SUM(CASE 
        WHEN timestamp >= date((SELECT MAX(timestamp) FROM "vis.oper_10min"), 'start of month') THEN power
        ELSE 0 
    END)/6 AS energy_mtd,
    SUM(CASE 
        WHEN timestamp >= datetime((SELECT MAX(timestamp) FROM "vis.oper_10min"), 'start of year') THEN power
        ELSE 0 
    END)/6 AS energy_ytd
FROM "vis.oper_10min"
GROUP BY id_wtg_complete;