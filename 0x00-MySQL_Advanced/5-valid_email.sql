-- Create a trigger to reset valid_email if the email has been changed
DELIMITER //

CREATE TRIGGER before_email_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- Check if the email is being changed
    IF NEW.email <> OLD.email THEN
        -- Reset valid_email to 0 if email has changed
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;