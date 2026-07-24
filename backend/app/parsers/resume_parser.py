import re


class ResumeParser:

    @staticmethod
    def parse(text: str):

        data = {
            "name": None,
            "email": None,
            "phone": None,
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
            "certifications": [],
            "languages": []
        }

        # Email
        email = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        if email:
            data["email"] = email.group()

        # Phone
        phone = re.search(
            r"(\+91[- ]?)?[6-9]\d{9}",
            text,
        )

        if phone:
            data["phone"] = phone.group()

        # Name (temporary logic)
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        if lines:
            data["name"] = lines[0]

        return data