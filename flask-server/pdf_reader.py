import re
from pdfminer.high_level import extract_pages, extract_text

def extract_file():
    text= extract_text("Script.pdf")
    return text

