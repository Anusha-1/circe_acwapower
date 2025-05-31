SELECT *
FROM "raw.input_10min" t 
WHERE t.ttimestamp >= :start and t.ttimestamp <= :end