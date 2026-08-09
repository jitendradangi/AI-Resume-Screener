-- Add missing ai_analysis column to resume_analysis table
ALTER TABLE resume_analysis ADD COLUMN ai_analysis JSON NULL;
