SELECT *
FROM [raw].[static_alarms_Azerbaijan] sa 
WHERE sa.Detected <= :end AND (sa.Detected > :start_det OR sa."Reset/Run"> :end_det) 