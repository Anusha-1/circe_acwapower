SELECT *
FROM "raw.static_met_mast_Kh-M1" t
WHERE t.PCTimeStamp >= :start AND t.PCTimeStamp <= :end