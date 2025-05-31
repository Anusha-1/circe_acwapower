DELETE FROM "intermediate.basic_10min"
WHERE (id_wtg_complete, timestamp) IN (
	SELECT te.id_wtg_complete, te.timestamp
	FROM "intermediate.basic_10min" te
	JOIN "intermediate.10min_horizons_basic" h ON te.id_wtg_complete = h.id_wtg_complete
	WHERE te.timestamp > h.horizon_datetime
);

