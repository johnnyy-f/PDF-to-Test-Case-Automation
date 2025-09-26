# PDF2Test: Automated Test Case Extraction

A tool that automates the extraction of verifiable test cases from technical documents (including: PDFs, Word, LaTeX) and lays the groundwork for code-level validation. This project blends document understanding, NLP, and structured data generation.

### **💡 Key Features**

* **Document Analysis:** Parses documentation formats including PDF, Word, and LaTeX.
* **Intelligent Extraction:** Leverages Large Language Models (LLMs) to identify and extract relevant test cases from unstructured text.
* **Structured Output:** Generates clear, actionable test cases in a standard JSON format.
* **Core Test Case Types:** Specifically designed to identify and extract:
    * Test cases on **modelling approach** and **implementation** (e.g., verifying a specific formula or methodology).
    * Test cases confirming **default parameters** and their values.
    * Test cases on **model scope** (e.g., which products and entities are in-scope).
    * Test cases for **inputs** (e.g., historical data range, valid input values, calibration frequency).

### **How It Works**

The core process is a three-step pipeline:

1.  **Document Loading:** The tool loads the PDF document using `PyPDFLoader`, extracting all text content.
2.  **Text Chunking:** The full text is segmented into smaller, manageable chunks using a `RecursiveCharacterTextSplitter`. This allows the LLM to process the document piece-by-piece.
3.  **LLM-Powered Extraction:** Each chunk is passed to an LLM along with a detailed prompt. The LLM then analyzes the text and extracts any verifiable statements as structured test cases, such as equations, parameters, and scope definitions.

### API Key and Endpoint Configuration

This project requires access to an Azure OpenAI instance.  
All sensitive credentials (API keys, endpoints) should be stored in a local `.env` file and **must not** be committed to Git.  
Make sure `.env` is included in your `.gitignore`.

#### Example `.env` file

```bash
AZURE_OPENAI_API_KEY="your_api_key_here"
AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"

AZURE_OPENAI_API_VERSION="your_api_version"
COMPLETION_DEPLOYMENT_NAME="your_deployment_name"
```

### **📦 Installation**

To get started, clone the repository and install the required dependencies.

```bash
# Clone the project repository
git clone [https://github.com/johnnyy-f/PDF-to-Test-Case-Automation.git]

# Install all necessary Python libraries
pip install -r requirements.txt
```

#### 1) Running with a Default Document
```bash
# Processes the default PDF file
python -m src.test_case_generator
```
#### 2) Processing a Custom Document
```bash
# Example for a file in your current directory
python -m src.test_case_generator --pdf_path "new_document.pdf"

# Example for a file in a different folder (use quotes for paths with spaces)
python -m src.test_case_generator --pdf_path "C:\Users\YourName\Documents\Another_Doc.pdf"
```
