import sys
import os

# Add backend directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.session import SessionLocal
from app.models.user import User

def check_users():
    db = SessionLocal()
    users = db.query(User).all()
    print(f"Found {len(users)} users in database:")
    for u in users:
        print(f"ID: {u.id} | Email: {u.email} | Hash: {u.password_hash[:15]}... (Len: {len(u.password_hash)})")
    db.close()

if __name__ == "__main__":
    check_users()
