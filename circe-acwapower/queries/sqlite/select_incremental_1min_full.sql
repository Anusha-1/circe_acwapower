
SELECT i.*
FROM "intermediate.input_1min" i
WHERE  i.timestamp > :time_limit;