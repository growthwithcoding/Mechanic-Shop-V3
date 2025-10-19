-- Recreate Database Script for Mechanic Shop V3
-- This script drops and recreates the database with all tables

-- Drop database if exists and create fresh
DROP DATABASE IF EXISTS mechanic_shop_v3;
CREATE DATABASE mechanic_shop_v3;
USE mechanic_shop_v3;

-- Note: Flask-Migrate will create the tables
-- Run this script first, then run: flask db upgrade
-- This ensures a clean database state

SELECT 'Database recreated successfully. Run flask db upgrade to create tables.' AS message;
