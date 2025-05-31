DELETE FROM [raw].[realtime_input_10min_Azerbaijan]
WHERE [datetime] < :start
