WITH total_counts AS (
    SELECT
        "sector_name",
        COUNT(*) AS total_count
    FROM
        "intermediate.basic_10min"
    GROUP BY
        sector_name
),
code_counts AS (
    SELECT
        "sector_name",
        "code",
        COUNT(*) AS code_count
    FROM
        "intermediate.basic_10min"
    WHERE "id_wf" = 1
    GROUP BY
        "sector_name",
        "code"
)
SELECT
    cc.sector_name,
    cc.code,
    cc.code_count,
    tc.total_count,
    (cc.code_count * 100.0 / tc.total_count) AS percentage
FROM
    code_counts cc
JOIN
    total_counts tc
ON
    cc.sector_name = tc.sector_name
ORDER BY
    cc.sector_name,
    percentage DESC;