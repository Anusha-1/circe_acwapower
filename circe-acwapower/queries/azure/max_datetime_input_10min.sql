SELECT MAX([timestamp])
FROM [intermediate].[input_10min]
WHERE id_wf = :wind_farm_id
