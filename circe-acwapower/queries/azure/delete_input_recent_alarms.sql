DELETE
FROM [intermediate].[input_alarms]
WHERE (start_datetime > :max_datetime OR end_datetime > :max_datetime OR end_datetime IS NULL) AND id_wf = :wind_farm_id