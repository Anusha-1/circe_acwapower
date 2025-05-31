DELETE FROM [raw].[realtime_met_mast_Az-M1]
WHERE [datetime] < :start
