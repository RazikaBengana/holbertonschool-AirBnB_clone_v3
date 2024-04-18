-- Create the database 'hbnb_test_db' if it does not already exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user 'hbnb_test'@'localhost' with a specified password if it does not already exist
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant all privileges on the database 'hbnb_test_db' to the user 'hbnb_test'@'localhost'
GRANT ALL PRIVILEGES ON `hbnb_test_db`.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on all tables in 'performance_schema' to the user 'hbnb_test'@'localhost'
GRANT SELECT ON `performance_schema`.* to 'hbnb_test'@'localhost';

-- Apply all privilege changes made above
FLUSH PRIVILEGES;