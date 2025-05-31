WITH max_timestamps AS (
    SELECT met_mast_id, MAX(timestamp) AS max_timestamp
    FROM 'vis.oper_met_mast'
    GROUP BY met_mast_id
)
SELECT t.*
FROM 'vis.oper_met_mast' AS t
JOIN max_timestamps AS mt
ON t.met_mast_id = mt.met_mast_id
AND t.timestamp = mt.max_timestamp;