-- Initialize FitTrack database
-- This script runs automatically when the MySQL container starts for the first time

-- Ensure the database exists
CREATE DATABASE IF NOT EXISTS fittrack;

-- Switch to the fittrack database
USE fittrack;

-- Grant permissions to the fittrack_user
GRANT ALL PRIVILEGES ON fittrack.* TO 'fittrack_user'@'%';
FLUSH PRIVILEGES;

-- The Flask application will create the tables automatically when it starts