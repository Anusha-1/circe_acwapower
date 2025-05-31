SELECT *
FROM [raw].[input_1min] t
WHERE t.ttimestamp >= :start AND t.ttimestamp <= :end