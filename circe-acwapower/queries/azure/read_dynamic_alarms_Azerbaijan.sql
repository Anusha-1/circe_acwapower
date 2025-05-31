SELECT *
FROM [raw].[realtime_alarms_Azerbaijan] sa 
WHERE sa.Detected > :max_datetime OR sa.[Reset/Run] > :max_datetime OR sa.[Reset/Run] IS NULL