DELETE FROM intermediate.basic_alarms
WHERE EXISTS (
    SELECT 1
    FROM intermediate.basic_alarms te
    JOIN intermediate.alarms_horizons_basic h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE intermediate.basic_alarms.id_wtg_complete = te.id_wtg_complete
      AND intermediate.basic_alarms.end_datetime = te.end_datetime
      AND te.end_datetime > h.horizon_datetime
);
