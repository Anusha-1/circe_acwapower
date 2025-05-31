DELETE FROM intermediate.wind_speed_corrections
WHERE EXISTS (
    SELECT 1
    FROM intermediate.wind_speed_corrections te
    JOIN intermediate.[10min_horizons_basic] h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE intermediate.wind_speed_corrections.id_wtg_complete = te.id_wtg_complete
      AND intermediate.wind_speed_corrections.timestamp = te.timestamp
      AND te.timestamp > h.horizon_datetime
);

