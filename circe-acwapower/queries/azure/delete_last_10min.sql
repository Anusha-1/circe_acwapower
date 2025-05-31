DELETE FROM [vis].[oper_10min]
WHERE EXISTS (
    SELECT 1
    FROM [vis].[oper_10min] te_inner
    JOIN [intermediate].[10min_horizons] h ON te_inner.[id_wtg_complete] = h.[id_wtg_complete]
    WHERE [vis].[oper_10min].[id_wtg_complete] = te_inner.[id_wtg_complete]
      AND [vis].[oper_10min].[timestamp] = te_inner.[timestamp]
      AND te_inner.[timestamp] > h.[horizon_datetime]
);
