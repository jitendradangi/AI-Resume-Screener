from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.repositories.user import user_repository
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
    ) -> User:

        if user_repository.email_exists(self.db, email):
            raise ValueError("Email already registered.")

        hashed_password = hash_password(password)

        return user_repository.create(
            self.db,
            full_name=full_name,
            email=email,
            password_hash=hashed_password,
        )

    def authenticate_user(
        self,
        email: str,
        password: str,
    ):
        user = user_repository.get_by_email(
            self.db,
            email,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        access_token = create_access_token(
            {
                "sub": user.public_id,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
        }

    def get_user(
        self,
        public_id: str,
    ) -> User | None:
        return user_repository.get_by_public_id(
            self.db,
            public_id,
        )

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        return user_repository.get_by_email(
            self.db,
            email,
        )