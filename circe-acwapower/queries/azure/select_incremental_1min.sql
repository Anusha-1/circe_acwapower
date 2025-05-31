
SELECT i.*
FROM intermediate.input_1min i
JOIN intermediate.[1min_horizons] h ON i.id_wtg_complete = h.id_wtg_complete
WHERE i.timestamp > h.horizon_datetime AND i.timestamp > :time_limit;