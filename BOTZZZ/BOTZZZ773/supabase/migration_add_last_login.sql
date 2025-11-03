-- Migration: Add last_login column to users table
-- Run this in your Supabase SQL Editor to update existing database

-- Add last_login column if it doesn't exist
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP WITH TIME ZONE;

-- Optionally set initial value to created_at for existing users
UPDATE users 
SET last_login = created_at 
WHERE last_login IS NULL;
