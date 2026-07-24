from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import user_repository
from app.services.base import BaseService
from app.utils.security import (
    hash_password,
    verify_password,
)


class UserService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:

        if user_repository.email_exists(self.db, email):
            raise ValueError("Email already registered.")

        if user_repository.username_exists(self.db, username):
            raise ValueError("Username already exists.")

        hashed_password = hash_password(password)

        return user_repository.create(
            self.db,
            username=username,
            email=email,
            hashed_password=hashed_password,
        )

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User | None:

        user = user_repository.get_by_email(
            self.db,
            email,
        )

        if not user:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None

        return user

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


user_service = UserService