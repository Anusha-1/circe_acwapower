SELECT 
	MAX([Detected]) AS start_time,
	MAX([Reset/Run]) AS end_time 
FROM [raw].[realtime_alarms_Azerbaijan]