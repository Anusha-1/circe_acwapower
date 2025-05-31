SELECT *
FROM [raw].[input_10min] t
WHERE t.ttimestamp >= :start AND t.ttimestamp <= :end