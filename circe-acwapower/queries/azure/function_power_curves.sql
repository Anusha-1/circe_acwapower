CREATE FUNCTION vis.fn_power_curve_customperiod
(
    @date_ini DATETIME,
    @date_fin DATETIME,
    @density VARCHAR(10)
)
RETURNS TABLE
AS
RETURN
(
    SELECT  
	        id_wtg_complete,  
	        sector_name,  
	        wind_speed,  
	        power,  
			density,
	        period,  
	        concept,  
	        CAST(1 AS BIT) AS reference,  
	        NULL AS timestamp  
	    FROM  
	        vis.interpolated_power_curves
	    WHERE density = @density
    UNION ALL
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
				WHERE density_corrected = @density
			) wsc
			ON o.id_wtg_complete = wsc.id_wtg_complete AND o.[timestamp] = wsc.[timestamp]   
	   WHERE  
	      o.timestamp BETWEEN @date_ini AND @date_fin
);