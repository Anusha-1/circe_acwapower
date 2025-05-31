SELECT 
    i.*
FROM "intermediate.basic_alarms" i
JOIN "intermediate.alarms_horizons" h ON i.id_wtg_complete = h.id_wtg_complete
JOIN "vis.alarms_metadata" m ON i.code = m.code 
WHERE i.end_datetime > h.horizon_datetime;
