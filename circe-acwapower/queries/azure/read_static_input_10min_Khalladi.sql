SELECT *
FROM [raw].[static_input_10min_Khalladi] t
WHERE t.ttimestamp >= :start AND t.ttimestamp <= :end