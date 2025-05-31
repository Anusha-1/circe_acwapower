SELECT
    t1.*
FROM
    "vis.treated_events" t1
    INNER JOIN (
        SELECT
            id_wtg_complete,
            MAX([start_datetime]) AS max_datetime
        FROM
            "vis.treated_events"
        GROUP BY
            id_wtg_complete
    ) t2 ON t1.id_wtg_complete = t2.id_wtg_complete
        AND t1.[start_datetime] = t2.max_datetime;
