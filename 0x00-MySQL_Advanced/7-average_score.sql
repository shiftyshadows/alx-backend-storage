-- Create the stored procedure ComputeAverageScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT DEFAULT 0;

    -- Calculate the average score for the given user_id, handling NULL if no scores exist
    SELECT COALESCE(AVG(score), 0) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average_score field in the users table with the calculated average
    UPDATE users
    SET average_score = avg_score
    WHERE id = user_id;
END //

DELIMITER ;
