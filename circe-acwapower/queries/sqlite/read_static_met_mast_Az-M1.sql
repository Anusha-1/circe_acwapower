SELECT *
FROM "raw.static_met_mast_Az-M1" t
WHERE t.PCTimeStamp >= :start AND t.PCTimeStamp <= :end