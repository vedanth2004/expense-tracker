import pytesseract
from PIL import Image
import io

class OCRProcessor:
    def extract_text(self, file) -> str:
        try:
            img = Image.open(file if hasattr(file, "read") else io.BytesIO(file))
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception:
            return ""
