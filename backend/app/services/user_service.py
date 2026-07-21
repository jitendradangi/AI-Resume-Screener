from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    user: UserCreate,
    hashed_password: str
):
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user