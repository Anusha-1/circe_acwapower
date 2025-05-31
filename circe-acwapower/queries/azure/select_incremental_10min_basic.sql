
SELECT i.*
FROM intermediate.basic_10min i
JOIN intermediate.[10min_horizons] h ON i.id_wtg_complete = h.id_wtg_complete
WHERE i.timestamp > h.horizon_datetime;