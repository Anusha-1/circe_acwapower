SELECT MAX([timestamp])
FROM [intermediate].[input_1min]
WHERE id_wf = :wind_farm_id
