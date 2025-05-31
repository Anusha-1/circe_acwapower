WITH corrections_to_delete AS (
    SELECT te.id_wtg_complete, te.timestamp
    FROM "intermediate.wind_speed_corrections_1min" te
    JOIN "intermediate.1min_horizons" h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE te.timestamp > h.horizon_datetime
)
DELETE FROM "intermediate.wind_speed_corrections_1min"
WHERE (id_wtg_complete, timestamp) IN (
    SELECT id_wtg_complete, timestamp
    FROM corrections_to_delete
);
