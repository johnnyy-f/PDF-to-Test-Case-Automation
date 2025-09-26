import os
import json
import logging
from typing import List, Dict, Any
from openai import AzureOpenAI
from config.config import Config

logger = logging.getLogger(__name__)

class LLMHandler:
    """
    A class to handle interactions with the Azure OpenAI API.
    """
    def __init__(self, config: Config):
        """
        Initializes the LLMHandler with configuration settings.
        
        Args:
            config (Config): The configuration object.
        """
        self.config = config
        self._validate_config()
        self.client = AzureOpenAI(
            api_key=self.config.AZURE_OPENAI_API_KEY,
            api_version=self.config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=self.config.AZURE_OPENAI_ENDPOINT
        )

    def _validate_config(self):
        """Validates that necessary configuration parameters are set."""
        if not self.config.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY is not set.")
        if not self.config.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is not set.")
        if not self.config.COMPLETION_DEPLOYMENT_NAME:
            raise ValueError("COMPLETION_DEPLOYMENT_NAME is not set.")

    def get_test_cases_from_chunk(self, chunk_text: str) -> List[Dict[str, str]]:
        """
        Calls the LLM to extract test cases from a single text chunk.
        
        Args:
            chunk_text (str): The text chunk to analyze.
            
        Returns:
            List[Dict[str, str]]: A list of dictionaries, where each dict is a test case.
        """
        messages = [
            {"role": "system", "content": self.config.SYSTEM_PROMPT},
            {"role": "user", "content": self.config.USER_PROMPT_TEMPLATE.format(chunk_text=chunk_text)}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.config.COMPLETION_DEPLOYMENT_NAME,
                messages=messages,
                temperature=self.config.LLM_TEMPERATURE,
                top_p=self.config.LLM_TOP_P
            )
            response_content = response.choices[0].message.content
            
            # The LLM returne JSON, so we attempt to parse it
            try:
                test_cases = json.loads(response_content)
                if not isinstance(test_cases, list):
                    logger.warning("LLM response was not a list. Returning empty list.")
                    return []
                return test_cases
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from LLM response. Response: {response_content[:200]}...")
                return []
        
        except Exception as e:
            logger.error(f"An error occurred during API call: {e}", exc_info=True)
            return []