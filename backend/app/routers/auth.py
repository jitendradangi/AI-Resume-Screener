from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.session import get_db
from app.schemas.user import UserCreate, Token
from app.schemas.user import UserLogin
from app.services.user_service import (
    create_user,
    get_user_by_email
)
from app.core.security import (
    hash_password,
    verify_password
)
from app.core.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    print(user.password)
    print(len(user.password))
    hashed_password = hash_password(user.password)

    new_user = create_user(
        db,
        user,
        hashed_password
    )

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.full_name,
            "email": new_user.email
        }
    }

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username.strip()
    print(f"Login attempt for email: '{email}'")
    db_user = get_user_by_email(db, email)

    if not db_user:
        print("User not found in database!")
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    print("User found. Verifying password...")
    if not verify_password(
        form_data.password,
        db_user.password_hash
    ):
        print("Password verification failed!")
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }