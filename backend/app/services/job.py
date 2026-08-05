from sqlalchemy.orm import Session

from app.models.job import Job
from app.repositories.job import job_repository
from app.repositories.user import user_repository
from app.services.base import BaseService
from app.parsers.job_parser import JobParser


class JobService(BaseService):
    def __init__(self, db: Session):
        super().__init__(db)

    def create_job(
        self,
        user_public_id: str,
        title: str,
        company: str,
        location: str | None = None,
        description: str | None = None,
        required_skills: list[str] | None = None,
        experience: str | None = None,
        education: str | None = None,
        employment_type: str | None = None,
        salary: str | None = None,
        status: str = "DRAFT",
    ) -> Job:
        user = user_repository.get_by_public_id(self.db, user_public_id)
        if not user:
            raise ValueError("User not found.")

        from app.models.enums import EmploymentType, JobStatus

        employment_type_enum = None
        if employment_type:
            try:
                employment_type_enum = EmploymentType(employment_type.upper())
            except ValueError:
                raise ValueError(f"Invalid employment type: {employment_type}")

        status_enum = None
        if status:
            try:
                status_enum = JobStatus(status.upper())
            except ValueError:
                raise ValueError(f"Invalid job status: {status}")

        return job_repository.create(
            self.db,
            user_id=user.id,
            title=title,
            company=company,
            location=location,
            description=description,
            required_skills=required_skills,
            experience=experience,
            education=education,
            employment_type=employment_type_enum,
            salary=salary,
            status=status_enum or JobStatus.DRAFT,
        )

    def get_job(
        self,
        public_id: str,
    ) -> Job | None:
        return job_repository.get_by_public_id(
            self.db,
            public_id,
        )

    def get_user_jobs(
        self,
        user_public_id: str,
    ) -> list[Job]:
        user = user_repository.get_by_public_id(
            self.db,
            user_public_id,
        )

        if not user:
            raise ValueError("User not found.")

        return job_repository.get_by_user(
            self.db,
            user.id,
        )

    def update_job(
        self,
        public_id: str,
        user_id: int,
        title: str | None = None,
        company: str | None = None,
        location: str | None = None,
        description: str | None = None,
        required_skills: list[str] | None = None,
        experience: str | None = None,
        education: str | None = None,
        employment_type: str | None = None,
        salary: str | None = None,
        status: str | None = None,
    ) -> Job:
        job = job_repository.get_by_public_id(self.db, public_id)
        if not job:
            raise ValueError("Job not found.")
        if job.user_id != user_id:
            raise PermissionError("Unauthorized to update this job.")

        update_kwargs = {}
        if title is not None:
            update_kwargs["title"] = title
        if company is not None:
            update_kwargs["company"] = company
        if location is not None:
            update_kwargs["location"] = location
        if description is not None:
            update_kwargs["description"] = description
        if required_skills is not None:
            update_kwargs["required_skills"] = required_skills
        if experience is not None:
            update_kwargs["experience"] = experience
        if education is not None:
            update_kwargs["education"] = education
        if employment_type is not None:
            from app.models.enums import EmploymentType
            try:
                update_kwargs["employment_type"] = EmploymentType(employment_type.upper())
            except ValueError:
                raise ValueError(f"Invalid employment type: {employment_type}")
        if salary is not None:
            update_kwargs["salary"] = salary
        if status is not None:
            from app.models.enums import JobStatus
            try:
                update_kwargs["status"] = JobStatus(status.upper())
            except ValueError:
                raise ValueError(f"Invalid job status: {status}")

        return job_repository.update(self.db, job, **update_kwargs)

    def delete_job(
        self,
        public_id: str,
        user_id: int,
    ) -> None:
        job = job_repository.get_by_public_id(self.db, public_id)
        if not job:
            raise ValueError("Job not found.")
        if job.user_id != user_id:
            raise PermissionError("Unauthorized to delete this job.")

        job_repository.delete(self.db, job)

    def get_open_jobs(
        self,
    ) -> list[Job]:
        return job_repository.get_open_jobs(self.db)

    def search_jobs(
        self,
        title: str | None = None,
        company: str | None = None,
        location: str | None = None,
    ) -> list[Job]:
        jobs = []

        if title:
            jobs.extend(job_repository.search_by_title(self.db, title))
        if company:
            jobs.extend(job_repository.search_by_company(self.db, company))
        if location:
            jobs.extend(job_repository.search_by_location(self.db, location))

        # Remove duplicates while preserving order
        seen = set()
        unique_jobs = []
        for job in jobs:
            if job.id not in seen:
                seen.add(job.id)
                unique_jobs.append(job)

        return unique_jobs

    def parse_job_description(
        self,
        public_id: str,
    ) -> dict:
        """
        Parse job description and extract structured information.

        Args:
            public_id: Public ID of the job

        Returns:
            Dict with parsed job data including:
                - required_skills: list of required skills
                - required_experience: extracted experience requirements
                - required_education: extracted education requirements
                - responsibilities: list of responsibilities
                - preferred_skills: list of preferred skills
        """
        job = self.get_job(public_id)
        if not job:
            raise ValueError("Job not found.")

        if not job.description:
            return {
                "required_skills": [],
                "required_experience": None,
                "required_education": None,
                "responsibilities": [],
                "preferred_skills": [],
            }

        # Parse the job description
        parsed_data = JobParser.parse_job_description(job.description)

        # Update the job with parsed data
        job_repository.update(
            self.db,
            job,
            parsed_required_skills=parsed_data["required_skills"],
            parsed_required_experience=parsed_data["required_experience"],
            parsed_required_education=parsed_data["required_education"],
            parsed_responsibilities=parsed_data["responsibilities"],
            parsed_preferred_skills=parsed_data["preferred_skills"],
        )

        return {
            "public_id": str(job.public_id),
            "parsed_data": parsed_data,
        }


job_service = JobService
