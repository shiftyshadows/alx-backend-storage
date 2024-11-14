-- Select band name and calculate lifespan for bands with 'Glam rock' in style
SELECT band_name,
       IFNULL(2022 - formed, 0) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;