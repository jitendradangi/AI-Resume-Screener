import fitz  # PyMuPDF


class PDFParser:
    @staticmethod
    def extract_text(file_path: str) -> str:
        text = ""

        try:
            with fitz.open(file_path) as pdf:
                for page in pdf:
                    text += page.get_text()

            return text.strip()

        except Exception as e:
            raise ValueError(f"Unable to parse PDF: {str(e)}")