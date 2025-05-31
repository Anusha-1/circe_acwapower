SELECT *
FROM [raw].[static_alarms] sa 
WHERE sa.Detected <= :end AND (sa.Detected > :start_det OR sa."Reset/Run"> :end_det) 