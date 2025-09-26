import os
import logging
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader

logger = logging.getLogger(__name__)

# Ben's Option of PDF Loader
def load_pdf_with_pypdf(file_path: str) -> str:
    """
    Loads text from a PDF file using PyPDFLoader.
    
    Args:
        file_path (str): The path to the PDF document.
        
    Returns:
        str: The concatenated text from all pages of the PDF.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        ImportError: If required libraries are not installed.
        Exception: For any other unexpected errors.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
    
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        full_text = " ".join(doc.page_content for doc in documents)
        logger.info(f"Successfully loaded {len(documents)} pages from '{file_path}'.")
        return full_text
    except ImportError:
        raise ImportError("Please make sure you have installed the required libraries with 'pip install langchain-community pypdf'")
    except Exception as e:
        logger.error(f"An unexpected error occurred during PDF loading: {e}", exc_info=True)
        raise

# Option 2 for loading .pdf files
def load_pdf_with_pdfplumber(file_path: str) -> str:
    """
    Loads text from a PDF file using pdfplumber.
    
    Args:
        file_path (str): The path to the PDF document.
        
    Returns:
        str: The concatenated text from all pages of the PDF.
    
    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")

    with pdfplumber.open(file_path) as pdf:
        full_text = "".join(page.extract_text() for page in pdf.pages)
        logger.info(f"Successfully loaded text from PDF using pdfplumber.")
    return full_text