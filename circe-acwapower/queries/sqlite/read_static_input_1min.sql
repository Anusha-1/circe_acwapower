SELECT *
FROM "raw.input_1min" t 
WHERE t.ttimestamp >= :start and t.ttimestamp <= :end