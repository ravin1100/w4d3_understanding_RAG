import pdfplumber
from typing import Dict, Any

def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    """Extract text from a PDF file with metadata.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        Dict[str, Any]: Dictionary containing extracted text and metadata
    """
    text = ""
    metadata = {}
    num_pages = 0
    
    try:
        with pdfplumber.open(file_path) as pdf:
            # Extract metadata
            metadata = {
                "title": pdf.metadata.get("Title", ""),
                "author": pdf.metadata.get("Author", ""),
                "creator": pdf.metadata.get("Creator", ""),
                "producer": pdf.metadata.get("Producer", ""),
                "num_pages": len(pdf.pages)
            }
            num_pages = len(pdf.pages)
            
            # Extract text from each page
            for page in pdf.pages:
                text += page.extract_text() + "\n\n"
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    return {
        "text": text.strip(),
        "metadata": metadata,
        "num_pages": num_pages,
        "char_count": len(text),
        "success": True
    }

def get_pdf_preview(text: str, max_chars: int = 500) -> str:
    """Get a preview of the PDF text.
    
    Args:
        text (str): Full text from PDF
        max_chars (int): Maximum number of characters to show
        
    Returns:
        str: Preview text
    """
    if len(text) <= max_chars:
        return text
    
    preview = text[:max_chars]
    last_period = preview.rfind(".")
    
    if last_period > 0:
        preview = preview[:last_period + 1]
    
    return f"{preview.strip()}..." 