SELECT *
FROM "raw.static_pitch_Azerbaijan" sa 
WHERE sa.PCTimeStamp <= :end AND sa.PCTimeStamp > :max  