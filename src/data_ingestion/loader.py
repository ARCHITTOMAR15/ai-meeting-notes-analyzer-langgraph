
from pathlib import Path
from llama_index.core.schema import Document


class TranscriptLoader:
    @staticmethod
    def load_document(file_path: str):
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".txt":
            text = path.read_text(encoding="utf-8")

        elif suffix == ".docx":
            from docx import Document as DocxDocument

            doc = DocxDocument(file_path)
            text = "\n".join(p.text for p in doc.paragraphs)

        elif suffix == ".pdf":
            from PyPDF2 import PdfReader

            reader = PdfReader(file_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)

        else:
            raise ValueError(f"Unsupported file format: {suffix}")

        return Document(text=text)


