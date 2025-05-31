WITH corrections_to_delete AS (
    SELECT te.id_wtg_complete, te.timestamp
    FROM "intermediate.wind_speed_corrections" te
    JOIN "intermediate.10min_horizons_basic" h ON te.id_wtg_complete = h.id_wtg_complete
    WHERE te.timestamp > h.horizon_datetime
)
DELETE FROM "intermediate.wind_speed_corrections"
WHERE (id_wtg_complete, timestamp) IN (
    SELECT id_wtg_complete, timestamp
    FROM corrections_to_delete
);
