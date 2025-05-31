SELECT 
	p.id_wf,
	MAX(p."timestamp") AS max_timestamp
FROM intermediate.pitch_with_lambda p
GROUP BY p.id_wf