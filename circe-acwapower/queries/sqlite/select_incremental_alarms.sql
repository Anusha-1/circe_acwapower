SELECT 
    i.*, 
    m.severity_scale as severity_scale,
	m.legacy_type as legacy_type,
	m.component as component,
	m.classification as classification,
	m.manufacturer_availability as manufacturer_availability,
	m.priority as priority
FROM "intermediate.input_alarms" i
JOIN "intermediate.alarms_horizons_basic" h ON i.id_wtg_complete = h.id_wtg_complete
JOIN "vis.alarms_metadata" m ON i.code = m.code 
WHERE i.end_datetime > h.horizon_datetime OR i.end_datetime ISNULL;
