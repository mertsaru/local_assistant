import pytesseract
from PIL import Image 

def transform_to_text(file_path: str, language):
    with Image.open(file_path) as img:
        text = pytesseract.image_to_string(img, lang=language)
    return text