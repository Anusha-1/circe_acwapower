SELECT
    t1.*
FROM
    "vis.oper_10min" t1
    JOIN (
        SELECT
            id_wtg_complete,
            MAX(timestamp) AS max_datetime
        FROM
            "vis.oper_10min"
        GROUP BY
            id_wtg_complete
    ) t2 ON t1.id_wtg_complete = t2.id_wtg_complete
        AND t1.timestamp = t2.max_datetime;