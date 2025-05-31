SELECT MAX([timestamp])
FROM "intermediate.tower_acceleration"
WHERE id_wf = :wind_farm_id
