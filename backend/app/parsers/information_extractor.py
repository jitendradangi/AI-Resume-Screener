"""
information_extractor.py
Converts raw section text (produced by SectionParser) into structured JSON
that can later be consumed by matching, ATS scoring, and AI analysis pipelines.
"""

import re
from typing import Any

from app.parsers.resume_parser import ResumeParser
from app.parsers.section_parse import SectionParser


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_lines(text: str) -> list[str]:
    """Return non-empty, stripped lines from a block of text."""
    return [l.strip() for l in text.splitlines() if l.strip()]


def _is_year(token: str) -> bool:
    """True if *token* looks like a 4-digit year (1950-2099)."""
    return bool(re.fullmatch(r"(19|20)\d{2}", token))


def _extract_year_range(text: str) -> dict[str, str | None]:
    """Return {start, end} from any substring like '2019 - 2022' or '2020 - Present'."""
    pattern = r"((?:19|20)\d{2})\s*[-]\s*((?:19|20)\d{2}|present|current|now)"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return {"start": m.group(1), "end": m.group(2).capitalize()}
    # single year fallback
    m2 = re.search(r"((?:19|20)\d{2})", text)
    if m2:
        return {"start": m2.group(1), "end": None}
    return {"start": None, "end": None}


# ---------------------------------------------------------------------------
# Public extractor class
# ---------------------------------------------------------------------------

class InformationExtractor:
    """
    Parses raw resume text sections into structured Python dicts / lists
    ready for JSON serialisation.
    """

    # ------------------------------------------------------------------
    # Skills
    # ------------------------------------------------------------------

    _SKILL_SEPARATORS = re.compile(r"[,;|]")

    _SKILL_NOISE = {
        "skills", "technical skills", "core skills", "key skills",
        "technologies", "tools", "frameworks", "languages",
        "proficient in", "familiar with", "experience with",
    }

    @classmethod
    def extract_skills(cls, skills_text: str) -> list[str]:
        """
        Return a deduplicated list of skill names from the skills section.
        Handles both comma-separated and one-per-line layouts.
        """
        if not skills_text:
            return []

        skills: list[str] = []
        for line in _split_lines(skills_text):
            parts = cls._SKILL_SEPARATORS.split(line)
            for part in parts:
                skill = part.strip().strip("*-o ").strip()
                if (
                    skill
                    and not skill.isdigit()
                    and skill.lower() not in cls._SKILL_NOISE
                    and len(skill) >= 2
                ):
                    skills.append(skill)

        # Deduplicate while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for s in skills:
            key = s.lower()
            if key not in seen:
                seen.add(key)
                unique.append(s)
        return unique

    # ------------------------------------------------------------------
    # Education
    # ------------------------------------------------------------------

    @classmethod
    def extract_education(cls, education_text: str) -> list[dict[str, Any]]:
        """
        Return a list of education entries.
        Each entry: {degree, institution, field, start, end, grade}
        """
        if not education_text:
            return []

        _DEGREE_KEYWORDS = re.compile(
            r"\b(b\.?tech|m\.?tech|b\.?e|m\.?e|bsc|msc|b\.?sc|m\.?sc|"
            r"bachelor|master|phd|ph\.?d|mba|diploma|associate|b\.?a|m\.?a|"
            r"b\.?com|m\.?com|bca|mca|be|me)\b",
            re.IGNORECASE,
        )

        entries: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        details: list[str] = []

        for line in _split_lines(education_text):
            year_range = _extract_year_range(line)
            is_year_line = year_range["start"] is not None
            has_degree = bool(_DEGREE_KEYWORDS.search(line))

            if has_degree or (is_year_line and current is None):
                if current is not None:
                    current["details"] = " ".join(details).strip() or None
                    entries.append(current)
                    details = []

                current = {
                    "degree": line if has_degree else None,
                    "institution": None,
                    "field": None,
                    "start": year_range["start"],
                    "end": year_range["end"],
                    "grade": None,
                }
            elif current is not None:
                grade_m = re.search(
                    r"(?:cgpa|gpa|grade|percentage|%)[:\s]*([\d.]+\s*%?)",
                    line,
                    re.IGNORECASE,
                )
                if grade_m:
                    current["grade"] = grade_m.group(1).strip()
                elif is_year_line:
                    if current["start"] is None:
                        current["start"] = year_range["start"]
                        current["end"] = year_range["end"]
                elif current["institution"] is None and len(line) > 3:
                    current["institution"] = line
                else:
                    details.append(line)

        if current is not None:
            current["details"] = " ".join(details).strip() or None
            entries.append(current)

        return entries

    # ------------------------------------------------------------------
    # Experience
    # ------------------------------------------------------------------

    @classmethod
    def extract_experience(cls, experience_text: str) -> list[dict[str, Any]]:
        """
        Return a list of work-experience entries.
        Each entry: {title, company, start, end, responsibilities}
        """
        if not experience_text:
            return []

        _AT_INDICATORS = re.compile(r"\bat\b|\bin\b|@", re.IGNORECASE)

        entries: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        responsibilities: list[str] = []

        for line in _split_lines(experience_text):
            year_range = _extract_year_range(line)
            has_year = year_range["start"] is not None

            is_entry_header = has_year or (
                bool(_AT_INDICATORS.search(line)) and len(line) < 120
            )

            if is_entry_header and (has_year or len(line) < 80):
                if current is not None:
                    current["responsibilities"] = responsibilities[:]
                    entries.append(current)
                    responsibilities = []

                split_m = re.split(r"\bat\b|@", line, maxsplit=1, flags=re.IGNORECASE)
                title_part = split_m[0].strip()
                company_part = split_m[1].strip() if len(split_m) > 1 else None

                title_clean = re.sub(
                    r"((?:19|20)\d{2})\s*[-]\s*((?:19|20)\d{2}|present|current|now)",
                    "",
                    title_part,
                    flags=re.IGNORECASE,
                ).strip(" -,")

                current = {
                    "title": title_clean or None,
                    "company": company_part,
                    "start": year_range["start"],
                    "end": year_range["end"],
                    "responsibilities": [],
                }
            elif current is not None:
                resp = line.lstrip("*- ").strip()
                if resp:
                    responsibilities.append(resp)

        if current is not None:
            current["responsibilities"] = responsibilities
            entries.append(current)

        return entries

    # ------------------------------------------------------------------
    # Projects
    # ------------------------------------------------------------------

    @classmethod
    def extract_projects(cls, projects_text: str) -> list[dict[str, Any]]:
        """
        Return a list of project entries.
        Each entry: {name, description, technologies, start, end}
        """
        if not projects_text:
            return []

        _TECH_PREFIX = re.compile(
            r"^(tech(?:nologies)?(?:\s*used)?|tools?|stack)[:\s-]+",
            re.IGNORECASE,
        )

        entries: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None
        desc_lines: list[str] = []

        for line in _split_lines(projects_text):
            year_range = _extract_year_range(line)
            has_year = year_range["start"] is not None

            is_header = (
                not line.startswith(("*", "-", "o "))
                and len(line) < 100
                and (has_year or current is None or len(line) < 60)
            )

            if is_header and not _TECH_PREFIX.match(line):
                if current is not None:
                    current["description"] = " ".join(desc_lines).strip() or None
                    entries.append(current)
                    desc_lines = []

                name = re.sub(
                    r"((?:19|20)\d{2})\s*[-]\s*((?:19|20)\d{2}|present|current|now)",
                    "",
                    line,
                    flags=re.IGNORECASE,
                ).strip(" -,|")

                current = {
                    "name": name or line,
                    "description": None,
                    "technologies": [],
                    "start": year_range["start"],
                    "end": year_range["end"],
                }
            elif current is not None:
                tech_m = _TECH_PREFIX.match(line)
                if tech_m:
                    tech_str = line[tech_m.end():]
                    current["technologies"] = [
                        t.strip()
                        for t in re.split(r"[,|;]", tech_str)
                        if t.strip()
                    ]
                else:
                    body = line.lstrip("*- ").strip()
                    if body:
                        desc_lines.append(body)

        if current is not None:
            current["description"] = " ".join(desc_lines).strip() or None
            entries.append(current)

        return entries

    # ------------------------------------------------------------------
    # Certifications
    # ------------------------------------------------------------------

    @classmethod
    def extract_certifications(cls, certifications_text: str) -> list[dict[str, Any]]:
        """
        Return a list of certification entries.
        Each entry: {name, issuer, year}
        """
        if not certifications_text:
            return []

        entries: list[dict[str, Any]] = []
        _ISSUED_BY = re.compile(r"\b(?:by|from|issued\s+by|via)\b", re.IGNORECASE)

        for line in _split_lines(certifications_text):
            line_clean = line.lstrip("*- ").strip()
            if not line_clean:
                continue

            year_m = re.search(r"((?:19|20)\d{2})", line_clean)
            year = year_m.group(1) if year_m else None

            name_part = re.sub(r"((?:19|20)\d{2})", "", line_clean).strip(" -,|")

            issuer_split = _ISSUED_BY.split(name_part, maxsplit=1)
            name = issuer_split[0].strip(" -,")
            issuer = issuer_split[1].strip(" -,") if len(issuer_split) > 1 else None

            if name:
                entries.append({"name": name, "issuer": issuer, "year": year})

        return entries

    # ------------------------------------------------------------------
    # Languages
    # ------------------------------------------------------------------

    @classmethod
    def extract_languages(cls, languages_text: str) -> list[dict[str, Any]]:
        """
        Return a list of language entries.
        Each entry: {language, proficiency}
        """
        if not languages_text:
            return []

        _PROFICIENCY_KEYWORDS = re.compile(
            r"\b(native|fluent|professional|intermediate|beginner|"
            r"basic|conversational|advanced|elementary|full\s+professional|"
            r"limited\s+working|mother\s+tongue)\b",
            re.IGNORECASE,
        )
        _SEPARATORS = re.compile(r"[,;|]")

        entries: list[dict[str, Any]] = []
        seen: set[str] = set()

        for line in _split_lines(languages_text):
            parts = _SEPARATORS.split(line)
            for part in parts:
                part = part.strip()
                if not part:
                    continue

                prof_m = _PROFICIENCY_KEYWORDS.search(part)
                proficiency = prof_m.group(0).capitalize() if prof_m else None
                lang = _PROFICIENCY_KEYWORDS.sub("", part).strip(" -,:()[]").strip()

                if lang and lang.lower() not in seen and len(lang) >= 2:
                    seen.add(lang.lower())
                    entries.append({"language": lang, "proficiency": proficiency})

        return entries

    # ------------------------------------------------------------------
    # Top-level entry point
    # ------------------------------------------------------------------

    @classmethod
    def extract_resume_data(cls, resume_text: str) -> dict[str, Any]:
        """
        Parse *resume_text* into fully structured JSON-serialisable data.

        Returns
        -------
        dict with keys:
            raw_sections   - the raw section texts from SectionParser
            summary        - str | None
            skills         - list[str]
            education      - list[dict]
            experience     - list[dict]
            projects       - list[dict]
            certifications - list[dict]
            languages      - list[dict]
        """
        sections: dict[str, str] = SectionParser.parse_sections(resume_text)

        return {
            "raw_sections": sections,
            "summary": sections.get("summary") or None,
            "skills": cls.extract_skills(sections.get("skills", "")),
            "education": cls.extract_education(sections.get("education", "")),
            "experience": cls.extract_experience(sections.get("experience", "")),
            "projects": cls.extract_projects(sections.get("projects", "")),
            "certifications": cls.extract_certifications(
                sections.get("certifications", "")
            ),
            "languages": cls.extract_languages(sections.get("languages", "")),
        }