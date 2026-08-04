from collections import defaultdict


class SectionParser:

    SECTION_HEADERS = {
        "summary": [
            "summary",
            "objective",
            "profile",
            "professional summary",
            "career objective",
            "about me",
        ],
        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "key skills",
            "technologies",
        ],
        "experience": [
            "experience",
            "work experience",
            "employment",
            "professional experience",
        ],
        "education": [
            "education",
            "academic",
            "academic background",
            "qualification",
        ],
        "projects": [
            "projects",
            "academic projects",
            "personal projects",
        ],
        "certifications": [
            "certifications",
            "certificates",
            "licenses",
        ],
        "languages": [
            "languages",
            "language",
        ],
    }

    @classmethod
    def parse_sections(cls, text: str) -> dict:

        sections = defaultdict(list)

        current_section = "general"

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines:

            lower_line = line.lower()

            found = False

            for section, headers in cls.SECTION_HEADERS.items():

                normalized = (
                    lower_line
                    .replace(":", "")
                    .replace("-", "")
                    .strip()
                )

                if normalized in headers:

                    current_section = section
                    found = True
                    break

            if found:
                continue

            sections[current_section].append(line)

        return {
            key: "\n".join(value)
            for key, value in sections.items()
        }