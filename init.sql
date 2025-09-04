-- Initialize HR AI Database
-- This script sets up the initial database configuration

-- Create database if it doesn't exist (handled by docker-compose)
-- CREATE DATABASE hr_ai_db;

-- Create user if it doesn't exist (handled by docker-compose)
-- CREATE USER hr_ai_user WITH PASSWORD 'hr_ai_password';

-- Grant privileges
-- GRANT ALL PRIVILEGES ON DATABASE hr_ai_db TO hr_ai_user;

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Create indexes for better performance (will be created by SQLAlchemy migrations)
-- These are just examples of what we might need

-- Full text search indexes
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_description_fts 
--   ON jobs USING gin(to_tsvector('english', description));

-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_candidates_skills_fts 
--   ON candidates USING gin(to_tsvector('english', skills));

-- Performance indexes
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_jobs_status_created 
--   ON jobs(status, created_at DESC);

-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_candidates_job_status 
--   ON candidates(job_id, status);

-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interviews_date_status 
--   ON interviews(scheduled_at, status);

-- Set timezone
SET timezone = 'Asia/Kolkata';
