-- Select the country of origin and total fans, grouped by origin
-- Then order the results by the total number of fans in descending order
SELECT origin, SUM(nb_fans) AS total_fans
FROM bands
GROUP BY origin
ORDER BY total_fans DESC;