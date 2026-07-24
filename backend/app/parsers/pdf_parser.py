import fitz

class PDFParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""

        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()

        return text.strip()