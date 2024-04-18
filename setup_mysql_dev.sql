-- Create a new database named 'hbnb_dev_db' if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create a new user 'hbnb_dev'@'localhost' with the specified password if the user does not already exist
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges to the user 'hbnb_dev' on all tables in the 'hbnb_dev_db' database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant the 'SELECT' privilege to the user 'hbnb_dev' on all tables in the 'performance_schema' database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Apply all the privilege changes made above
FLUSH PRIVILEGES;