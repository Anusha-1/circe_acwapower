DELETE FROM [vis].[oper_1min]
WHERE EXISTS (
    SELECT 1
    FROM [vis].[oper_1min] te_inner
    JOIN [intermediate].[1min_horizons] h ON te_inner.[id_wtg_complete] = h.[id_wtg_complete]
    WHERE [vis].[oper_1min].[id_wtg_complete] = te_inner.[id_wtg_complete]
      AND [vis].[oper_1min].[timestamp] = te_inner.[timestamp]
      AND te_inner.[timestamp] > h.[horizon_datetime]
);
