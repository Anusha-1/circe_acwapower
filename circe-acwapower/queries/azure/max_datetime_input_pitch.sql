SELECT MAX([timestamp])
FROM [intermediate].[pitch]
WHERE id_wf = :wind_farm_id
