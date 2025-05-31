SELECT  
    o.id_wtg_complete,  
    o.sector_name,  
    wsc.wind_speed_corrected AS wind_speed ,  
    o.power,  
	wsc.density_corrected AS density,
    'custom' AS period,  
    '10min data' AS concept,  
    CAST(0 AS BIT) AS reference,  
    o.timestamp  
FROM  
    vis.oper_10min AS o
JOIN
	(
		SELECT *
		FROM intermediate.wind_speed_corrections
		WHERE density_corrected = '1.12'
	) wsc
	ON o.id_wtg_complete = wsc.id_wtg_complete AND o.[timestamp] = wsc.[timestamp] 