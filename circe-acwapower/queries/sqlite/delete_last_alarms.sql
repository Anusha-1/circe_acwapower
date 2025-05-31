DELETE FROM "intermediate.alarms_with_losses"
WHERE (id_wtg_complete, end_datetime) IN (
	SELECT te.id_wtg_complete, te.end_datetime
	FROM "intermediate.alarms_with_losses" te
	JOIN "intermediate.alarms_horizons" h ON te.id_wtg_complete = h.id_wtg_complete
	WHERE te.end_datetime > h.horizon_datetime
);


