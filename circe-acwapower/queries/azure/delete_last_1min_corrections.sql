DELETE FROM intermediate.wind_speed_corrections_1min
WHERE EXISTS (
    SELECT 1
    FROM intermediate.wind_speed_corrections_1min te
    JOIN intermediate.[1min_horizons] h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE intermediate.wind_speed_corrections_1min.id_wtg_complete = te.id_wtg_complete
      AND intermediate.wind_speed_corrections_1min.timestamp = te.timestamp
      AND te.timestamp > h.horizon_datetime
);

