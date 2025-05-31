SELECT *
FROM "raw.static_input_1min_Khalladi" t
WHERE t.ttimestamp >= :start AND t.ttimestamp <= :end