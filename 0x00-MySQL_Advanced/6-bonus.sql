-- Create the stored procedure AddBonus
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if the project with the given name already exists
    SET project_id = (SELECT id FROM projects WHERE name = project_name LIMIT 1);

    -- If the project does not exist, insert it and retrieve the new project_id
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the new correction record for the user and project
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //

DELIMITER ;