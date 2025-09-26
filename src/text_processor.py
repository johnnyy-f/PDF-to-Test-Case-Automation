import re
import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Cleans and normalizes text for processing.
    
    Args:
        text (str): The raw text to be cleaned.
        
    Returns:
        str: The cleaned text.
    """
    logger.info("Cleaning and normalizing text...")
    text = text.replace('\xa0', ' ')
    text = re.sub(r'\n{2,}', '\n\n', text)
    text = re.sub(r'[\t]+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """
    Splits the document text into manageable chunks.
    
    Args:
        text (str): The full document text.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of characters to overlap between chunks.
        
    Returns:
        List[str]: A list of text chunks.
    """
    logger.info(f"Chunking text with size={chunk_size} and overlap={chunk_overlap}...")
    recursive_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = recursive_splitter.split_text(text)
    logger.info(f"Created {len(chunks)} chunks.")
    return chunks