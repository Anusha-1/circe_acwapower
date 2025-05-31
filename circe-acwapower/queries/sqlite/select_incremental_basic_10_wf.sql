SELECT 
    id_wtg_complete,
    timestamp,
    lambda_parameter
FROM "intermediate.basic_10min"
WHERE id_wf = :id_wf and timestamp > :timestamp