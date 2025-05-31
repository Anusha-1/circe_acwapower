DELETE FROM "intermediate.basic_alarms"
WHERE (id_wtg_complete, end_datetime) IN (
	SELECT te.id_wtg_complete, te.end_datetime
	FROM "intermediate.basic_alarms" te
	JOIN "intermediate.alarms_horizons_basic" h ON te.id_wtg_complete = h.id_wtg_complete
	WHERE te.end_datetime > h.horizon_datetime
);


