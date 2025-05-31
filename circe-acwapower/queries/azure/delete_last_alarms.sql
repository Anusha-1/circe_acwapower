DELETE FROM intermediate.alarms_with_losses
WHERE EXISTS (
    SELECT 1
    FROM intermediate.alarms_with_losses te
    JOIN intermediate.alarms_horizons h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE intermediate.alarms_with_losses.id_wtg_complete = te.id_wtg_complete
      AND intermediate.alarms_with_losses.end_datetime = te.end_datetime
      AND te.end_datetime > h.horizon_datetime
);
