"""
Database migration script to add missing ai_analysis column to resume_analysis table
"""
from app.database.db import engine
from sqlalchemy import text

def add_ai_analysis_column():
    """Add ai_analysis column to resume_analysis table if it doesn't exist"""
    try:
        with engine.connect() as connection:
            # Check if column already exists
            check_column = text("""
                SELECT COUNT(*) as count 
                FROM information_schema.columns 
                WHERE table_name = 'resume_analysis' 
                AND column_name = 'ai_analysis'
                AND table_schema = DATABASE()
            """)
            
            result = connection.execute(check_column).fetchone()
            
            if result[0] > 0:
                print("Column 'ai_analysis' already exists in resume_analysis table")
                return
            
            # Add the column
            alter_table = text("ALTER TABLE resume_analysis ADD COLUMN ai_analysis JSON NULL")
            connection.execute(alter_table)
            connection.commit()
            
            print("Successfully added 'ai_analysis' column to resume_analysis table")
            
    except Exception as e:
        print(f"Error adding column: {e}")
        raise

if __name__ == "__main__":
    add_ai_analysis_column()
