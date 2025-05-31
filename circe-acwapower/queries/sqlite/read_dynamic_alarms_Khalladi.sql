SELECT *
FROM "raw.realtime_alarms_Khalladi" sa 
WHERE sa.Detected > :max_datetime OR sa.[Reset/Run] > :max_datetime OR sa.[Reset/Run] ISNULL