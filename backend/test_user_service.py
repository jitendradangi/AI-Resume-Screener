from app.database.db import engine
from app.database.session import SessionLocal
from app.services.user import UserService
from app.core.security import hash_password
from sqlalchemy import text

db = SessionLocal()
service = UserService(db)

try:
    # Get the user with email
    result = db.execute(text('SELECT id, public_id, full_name, email FROM users WHERE email = "jitendradangi732@gmail.com"'))
    users = result.fetchall()
    if users:
        user_id = users[0][1]
        user = service.get_user(user_id)
        print(f'Found user: {user.full_name}, {user.email}')
        
        # Test schema serialization
        from app.schemas.user import UserResponse
        user_response = UserResponse.model_validate(user)
        print(f'Schema response: {user_response.full_name}, {user_response.email}')
        print(f'Full response: {user_response.model_dump()}')
        
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
finally:
    db.close()
