WITH CTE AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id_wtg_complete ORDER BY start_datetime DESC) AS rn
    FROM
        [vis].[treated_events]
)
SELECT
    *
FROM
    CTE
WHERE
    rn = 1;