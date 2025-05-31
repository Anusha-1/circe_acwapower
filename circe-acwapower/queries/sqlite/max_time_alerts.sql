SELECT MAX(start_datetime) AS start_time
FROM "intermediate.input_alarms"
WHERE id_wf = :wind_farm_id