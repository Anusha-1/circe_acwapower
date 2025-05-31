SELECT 
	pcm.*,
	pc.bin,
	pc.power,
	pc.sigma
FROM "vis.power_curves" pc
LEFT JOIN "vis.pc_metadata" pcm ON pc.pc_id = pcm.pc_id;