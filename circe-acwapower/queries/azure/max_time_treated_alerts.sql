SELECT 
	MAX([start_time]) AS start_time,
	MAX([end_time]) AS end_time 
FROM [raw].[realtime_alarms]