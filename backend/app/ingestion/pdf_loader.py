import os
import fitz  # PyMuPDF
from typing import List, Dict, Any

class PDFExtractionError(Exception):
    pass

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise PDFExtractionError(f"File not found: {file_path}")

    def extract_text_by_page(self) -> List[Dict[str, Any]]:
        """
        Extracts text from a PDF file page by page.
        Returns a list of dicts with keys: 'page_number', 'text', 'char_count', 'word_count'.
        """
        pages = []
        try:
            doc = fitz.open(self.file_path)
            if doc.is_encrypted:
                raise PDFExtractionError("PDF is encrypted and password protected.")
            
            if len(doc) == 0:
                raise PDFExtractionError("PDF contains 0 pages.")

            total_words = 0
            for i, page in enumerate(doc):
                text = page.get_text("text").strip()
                words = len(text.split())
                total_words += words
                pages.append({
                    "page_number": i + 1,
                    "text": text,
                    "char_count": len(text),
                    "word_count": words
                })
            
            doc.close()

            if total_words < 10:
                # Detect potentially scanned or empty PDF
                for p in pages:
                    p["warning"] = "Low text density detected (possible scanned/image PDF)."

            return pages

        except fitz.FileDataError as e:
            raise PDFExtractionError(f"Corrupted or invalid PDF file: {str(e)}")
        except Exception as e:
            if isinstance(e, PDFExtractionError):
                raise e
            raise PDFExtractionError(f"Failed to process PDF: {str(e)}")
