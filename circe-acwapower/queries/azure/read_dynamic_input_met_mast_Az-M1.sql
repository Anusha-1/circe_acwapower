SELECT *
FROM raw.[realtime_met_mast_Az-M1] t
WHERE t.datetime > :start