-- Migration: Add theme_id column to games table
-- Date: 2025-10-24
-- Description: Add theme support for random theme selection

-- Add theme_id column if it doesn't exist
ALTER TABLE games 
ADD COLUMN IF NOT EXISTS theme_id INTEGER DEFAULT 1;

-- Add comment
COMMENT ON COLUMN games.theme_id IS 'Theme ID from themes.py - determines role names for each round';

