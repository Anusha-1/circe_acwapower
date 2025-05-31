DELETE FROM "vis.oper_1min"
WHERE (id_wtg_complete, timestamp) IN (
	SELECT te.id_wtg_complete, te.timestamp
	FROM "vis.oper_1min" te
	JOIN "intermediate.1min_horizons" h ON te.id_wtg_complete = h.id_wtg_complete
	WHERE te.timestamp > h.horizon_datetime
);

