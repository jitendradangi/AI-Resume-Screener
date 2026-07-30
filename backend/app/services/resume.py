from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.repositories.resume import resume_repository
from app.repositories.user import user_repository
from app.services.base import BaseService
from pathlib import Path



class ResumeService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_resume(
        self,
        user_public_id: str,
        filename: str,
        original_filename: str,
        filepath: str,
        filetype: str,
        filesize: int,
    ) -> Resume:
        user = user_repository.get_by_public_id(self.db, user_public_id)
        if not user:
            raise ValueError("User not found.")

        return resume_repository.create(
            self.db,
            user_id=user.id,
            filename=filename,
            original_filename=original_filename,
            filepath=filepath,
            filetype=filetype,
            filesize=filesize,
        )

    def delete_resume(
        self,
        resume_id: int,
        user_id: int,
    ) -> None:
        resume = resume_repository.get_by_id(self.db, resume_id)
        if not resume:
            raise ValueError("Resume not found.")
        if resume.user_id != user_id:
            raise ValueError("Unauthorized to delete this resume.")
        resume_repository.delete(self.db, resume)

    def get_resume(
        self,
        public_id: str,
    ) -> Resume | None:
        return resume_repository.get_by_public_id(
            self.db,
            public_id,
        )

    def get_user_resumes(
        self,
        user_public_id: str,
    ) -> list[Resume]:

        user = user_repository.get_by_public_id(
            self.db,
            user_public_id,
        )

        if not user:
            raise ValueError("User not found.")

        return resume_repository.get_by_user(
            self.db,
            user.id,
        )

    def get_latest_resume(
        self,
        user_public_id: str,
    ) -> Resume | None:

        user = user_repository.get_by_public_id(
            self.db,
            user_public_id,
        )

        if not user:
            raise ValueError("User not found.")

        return resume_repository.get_latest_by_user(
            self.db,
            user.id,
        )
    


resume_service = ResumeService