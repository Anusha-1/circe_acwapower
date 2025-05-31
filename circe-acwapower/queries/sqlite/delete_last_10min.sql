DELETE FROM "vis.oper_10min"
WHERE (id_wtg_complete, timestamp) IN (
	SELECT te.id_wtg_complete, te.timestamp
	FROM "vis.oper_10min" te
	JOIN "intermediate.10min_horizons" h ON te.id_wtg_complete = h.id_wtg_complete
	WHERE te.timestamp > h.horizon_datetime
);

