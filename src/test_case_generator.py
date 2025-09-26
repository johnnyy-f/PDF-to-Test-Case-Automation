import os
import json
import argparse
import logging
from typing import List, Dict, Any
from config.config import Config
from src.data_loader import load_pdf_with_pypdf
from src.text_processor import clean_text, chunk_text
from src.llm_handler import LLMHandler

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_test_cases(pdf_path: str, output_path: str) -> None:
    """
    Main function to orchestrate the test case generation process.
    
    Args:
        pdf_path (str): Path to the input PDF file.
        output_path (str): Path to save the extracted test cases.
    """
    config = Config()
    
    try:
        # Step 1: Load and Clean Document
        logger.info(f"Starting process for PDF at: {pdf_path}")
        full_text = load_pdf_with_pypdf(pdf_path)
        cleaned_text = clean_text(full_text)
        
        # Step 2: Chunk the Document
        chunks = chunk_text(cleaned_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
        
        # Step 3: Initialize LLM Handler
        llm_handler = LLMHandler(config)
        
        # Step 4: Process Chunks with LLM
        all_test_cases: List[Dict[str, Any]] = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1} of {len(chunks)}...")
            test_cases = llm_handler.get_test_cases_from_chunk(chunk)
            
            if test_cases:
                all_test_cases.extend(test_cases)
                logger.info(f"Found {len(test_cases)} test cases in chunk {i+1}.")
            else:
                logger.info(f"No test cases found in chunk {i+1}.")
                
        # Step 5: Save Results
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
            
        with open(output_path, 'w') as f:
            json.dump(all_test_cases, f, indent=2)
            
        logger.info("--- Processing Complete ---")
        logger.info(f"Total test cases extracted: {len(all_test_cases)}")
        logger.info(f"Results saved to: {output_path}")

    except FileNotFoundError as e:
        logger.error(e)
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
    except Exception as e:
        logger.error(f"An unrecoverable error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    # Use argparse to make the script more flexible
    parser = argparse.ArgumentParser(description="Extracts test cases from a PDF document using an LLM.")
    parser.add_argument(
        "--pdf_path",
        type=str,
        default=Config.PDF_FILE_PATH,
        help="Path to the input PDF document."
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=Config.OUTPUT_FILE_PATH,
        help="Path to save the output JSON file."
    )
    
    args = parser.parse_args()
    
    generate_test_cases(args.pdf_path, args.output_path)