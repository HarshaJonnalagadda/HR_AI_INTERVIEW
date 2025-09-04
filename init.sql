-- This script is executed when the PostgreSQL container is first created.
-- It sets up necessary extensions and configurations within the hr_ai_db database.

-- The database itself is created automatically by the Docker entrypoint script
-- using the POSTGRES_DB environment variable.

-- Connect to the newly created database to run the following commands.
\c hr_ai_db

-- Enable required extensions for UUIDs, text search, and indexing.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Set the default timezone for the database session.
-- This ensures consistency in timestamp handling.
ALTER DATABASE hr_ai_db SET timezone TO 'Asia/Kolkata';
