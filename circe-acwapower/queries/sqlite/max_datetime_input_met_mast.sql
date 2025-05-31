SELECT MAX(timestamp)
FROM "vis.oper_met_mast"
WHERE met_mast_id = :met_mast_id
