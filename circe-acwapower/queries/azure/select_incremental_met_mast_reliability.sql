
SELECT i.*
FROM vis.oper_met_mast i
JOIN intermediate.[10min_horizons_reliability] h ON i.id_wtg_complete = h.id_wtg_complete
WHERE i.timestamp > h.horizon_datetime;