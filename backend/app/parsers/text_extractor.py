import os

from app.parsers.pdf_parser import PDFParser
from app.parsers.docx_parser import DOCXParser


class TextExtractor:

    @staticmethod
    def extract(file_path: str) -> str:

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return PDFParser.extract_text(file_path)

        elif extension in [".doc", ".docx"]:
            return DOCXParser.extract_text(file_path)

        raise ValueError("Unsupported file format")