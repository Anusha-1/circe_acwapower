SELECT *
FROM "raw.static_tower_acceleration_Khalladi" sa 
WHERE sa.PCTimeStamp <= :end AND sa.PCTimeStamp > :max  