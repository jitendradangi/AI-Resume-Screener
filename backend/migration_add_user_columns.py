from app.database.db import engine
from sqlalchemy import text

def add_user_profile_columns():
    """Add missing user profile columns to the database."""
    
    columns_to_add = [
        "ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL",
        "ALTER TABLE users ADD COLUMN location VARCHAR(100) NULL", 
        "ALTER TABLE users ADD COLUMN professional_title VARCHAR(100) NULL",
        "ALTER TABLE users ADD COLUMN skills VARCHAR(500) NULL"
    ]
    
    with engine.connect() as connection:
        for column_sql in columns_to_add:
            try:
                connection.execute(text(column_sql))
                connection.commit()
                print(f"SUCCESS: {column_sql}")
            except Exception as e:
                if "Duplicate column" in str(e):
                    print(f"SKIP: Column already exists: {column_sql}")
                else:
                    print(f"ERROR: {column_sql} - {e}")
    
    print("\nDatabase migration completed!")

if __name__ == "__main__":
    add_user_profile_columns()
