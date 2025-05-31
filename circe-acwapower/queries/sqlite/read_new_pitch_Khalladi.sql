SELECT *
FROM "raw.static_pitch_Khalladi" sa 
WHERE sa.PCTimeStamp <= :end AND sa.PCTimeStamp > :max  