SELECT *
FROM [raw].[static_tower_acceleration_Khalladi] sa
WHERE sa.PCTimeStamp <= :end
