import requests
import json
from app.database.db import engine
from app.database.session import SessionLocal
from app.services.user import UserService
from app.core.security import create_access_token
from sqlalchemy import text

db = SessionLocal()
service = UserService(db)

try:
    # Get the user
    result = db.execute(text('SELECT id, public_id, full_name, email FROM users WHERE email = "jitendradangi732@gmail.com"'))
    users = result.fetchall()
    if users:
        user_id = users[0][1]
        user = service.get_user(user_id)
        
        # Create a token for this user
        token = create_access_token({'sub': str(user.public_id)})
        print(f'Token: {token}')
        
        # Now test the API endpoint with this token
        headers = {'Authorization': f'Bearer {token}'}
        profile_response = requests.get('http://localhost:8000/user/profile', headers=headers)
        print(f'Profile response status: {profile_response.status_code}')
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            print(f'Profile response: {json.dumps(profile_data, indent=2)}')
        else:
            print(f'Profile error: {profile_response.text}')
        
except Exception as e:
    print('Error:', e)
    import traceback
    traceback.print_exc()
finally:
    db.close()
