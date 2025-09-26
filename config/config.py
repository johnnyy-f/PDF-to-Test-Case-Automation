import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class to manage project settings.
    """
    # --- File Paths ---
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Alter below path for input file
    PDF_FILE_PATH = os.path.join(BASE_DIR, 'data', 'Example PDF Docs', 'filtered-historical-simulation-value-at-risk-models-and-their-competitors.pdf')
    OUTPUT_FILE_PATH = os.path.join(BASE_DIR, 'output', 'extracted_test_cases.json')
    
    # --- LLM Settings ---
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
    COMPLETION_DEPLOYMENT_NAME = os.getenv("COMPLETION_DEPLOYMENT_NAME", "gpt-35-turbo")
    LLM_TEMPERATURE = 0.3
    LLM_TOP_P = 0.95
    
    # --- Chunking Settings ---
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    # --- LLM Prompts ---
    SYSTEM_PROMPT = """
    You are an expert AI assistant tasked with identifying and extracting potential test cases from a document. Your primary goal is to act as a quality assurance specialist, carefully reading the provided text to find specific, verifiable statements that describe functionality, equations, parameters, or model scope.

    A 'test case' is any material item that should be confirmed as correctly implemented. This includes:
    - Descriptions of the model's scope or purpose.
    - Key equations, formulas, or algorithms.
    - Specific parameter settings, variables, or data requirements.
    - Any defined functionality, constraints, or assumptions.
    - References to specific models, methodologies, or historical data.

    For each test case you identify, you must provide the following:
    - **Test Case Description:** A clear, concise summary of the test case.
    - **Reference Text:** The exact sentence or section from the original document that supports the test case.

    Format your output as a list of dictionaries in JSON format, with each dictionary representing a single test case. If no test cases are found, return an empty list.
    """
    
    USER_PROMPT_TEMPLATE = """
    Please analyze the following document excerpt and extract all potential test cases based on the instructions in the system prompt.

    Document Excerpt:
    ---
    {chunk_text}
    ---

    Test Cases (as a JSON array):
    """