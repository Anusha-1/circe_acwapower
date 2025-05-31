SELECT *
FROM "raw.static_alarms" sa 
WHERE sa.Detected <= :end