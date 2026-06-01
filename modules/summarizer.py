"""
Summarizer Module

This module provides functionality to summarize study notes into concise summaries,
key points, and important concepts.
"""

from typing import Dict, Any
from utils.ollama_client import OllamaClient
import logging

logger = logging.getLogger(__name__)


class Summarizer:
    """
    A class to summarize study notes using LLM.
    
    Attributes:
        client (OllamaClient): The Ollama client for API calls
        prompt_template (str): The prompt template for summarization
    """
    
    def __init__(self, client: OllamaClient, prompt_template: str) -> None:
        """
        Initialize the Summarizer.
        
        Args:
            client: OllamaClient instance for API calls
            prompt_template: Template for the summary prompt
        """
        self.client = client
        self.prompt_template = prompt_template
    
    def summarize(self, notes: str) -> Dict[str, Any]:
        """
        Summarize study notes.
        
        Args:
            notes: The study notes to summarize
        
        Returns:
            Dictionary containing summary, key_points, and important_concepts
        
        Raises:
            Exception: If summarization fails
        """
        if not notes or notes.strip() == "":
            raise ValueError("Notes cannot be empty")
        
        try:
            # Format prompt with notes
            prompt = self.prompt_template.format(notes=notes)
            
            logger.info("Starting summarization process")
            response = self.client.generate(prompt, temperature=0.5)
            
            if not response:
                raise Exception("No response from model")
            
            # Parse response
            result = self._parse_response(response)
            logger.info("Summarization completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Summarization failed: {str(e)}")
            raise
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response into structured format.
        
        Args:
            response: The raw response from LLM
        
        Returns:
            Dictionary with parsed sections
        """
        sections = {
            "summary": "",
            "key_points": [],
            "important_concepts": ""
        }
        
        try:
            # Split by section headers
            if "## Summary" in response:
                summary_section = response.split("## Summary")[1]
                if "## Key Points" in summary_section:
                    sections["summary"] = summary_section.split("## Key Points")[0].strip()
                else:
                    sections["summary"] = summary_section.split("## Important")[0].strip()
            
            # Extract key points
            if "## Key Points" in response:
                points_section = response.split("## Key Points")[1]
                if "## Important" in points_section:
                    points_text = points_section.split("## Important")[0].strip()
                else:
                    points_text = points_section.strip()
                
                # Extract bullet points
                for line in points_text.split("\n"):
                    line = line.strip()
                    if line and line.startswith("-"):
                        sections["key_points"].append(line[2:].strip())
            
            # Extract important concepts
            if "## Important Concepts" in response:
                concepts_section = response.split("## Important Concepts")[1].strip()
                sections["important_concepts"] = concepts_section
        
        except Exception as e:
            logger.warning(f"Error parsing response structure: {str(e)}")
            sections["summary"] = response
        
        return sections
