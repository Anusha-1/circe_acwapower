SELECT *
FROM [raw].[static_input_1min_Azerbaijan] t
WHERE t.ttimestamp >= :start AND t.ttimestamp <= :end