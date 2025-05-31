DELETE FROM [intermediate].[basic_10min]
WHERE EXISTS (
    SELECT 1
    FROM [intermediate].[basic_10min] te_inner
    JOIN [intermediate].[10min_horizons_basic] h ON te_inner.[id_wtg_complete] = h.[id_wtg_complete]
    WHERE [intermediate].[basic_10min].[id_wtg_complete] = te_inner.[id_wtg_complete]
      AND [intermediate].[basic_10min].[timestamp] = te_inner.[timestamp]
      AND te_inner.[timestamp] > h.[horizon_datetime]
);
