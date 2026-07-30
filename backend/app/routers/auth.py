from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import TokenResponse

from app.services.user import UserService
from app.schemas.auth import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    try:
        new_user = service.register_user(
            full_name=user.full_name,
            email=user.email,
            password=user.password,
        )

        return {
            "message": "User registered successfully",
            "user": new_user,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    result = service.authenticate_user(
        email=form_data.username.strip(),
        password=form_data.password,
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    return result