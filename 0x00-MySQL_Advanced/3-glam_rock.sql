-- Select band name and calculate lifespan for bands with 'Glam rock' in style
SELECT band_name,
       CASE 
           WHEN split IS NULL THEN 2022 - formed  -- If the band hasn't split, calculate lifespan to 2022
           ELSE split - formed                   -- If the band has split, calculate lifespan to the split year
       END AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
  AND formed IS NOT NULL                          -- Ensure 'formed' is not NULL to avoid calculation errors
ORDER BY lifespan DESC;

