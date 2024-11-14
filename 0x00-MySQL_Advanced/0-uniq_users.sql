-- Create the 'users' table only if it does not already exist
CREATE TABLE IF NOT EXISTS users (
    -- Define 'id' as an integer, non-nullable, auto-incrementing primary key
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    
    -- Define 'email' as a string up to 255 characters, non-nullable, and unique
    email VARCHAR(255) NOT NULL UNIQUE,
    
    -- Define 'name' as an optional string attribute up to 255 characters
    name VARCHAR(255)
);