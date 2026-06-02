"""
Summarizer Module

This module provides functionality to summarize study notes into concise summaries,
key points, and important concepts.
"""

from typing import Dict, Any
from utils.llm_factory import BaseLLMClient
import logging
import re

logger = logging.getLogger(__name__)


class Summarizer:
    """
    A class to summarize study notes using LLM.
    
    Attributes:
        client (BaseLLMClient): The LLM client for API calls
        prompt_template (str): The prompt template for summarization
    """
    
    def __init__(self, client: BaseLLMClient, prompt_template: str) -> None:
        """
        Initialize the Summarizer.
        
        Args:
            client: BaseLLMClient instance for API calls
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
            "summary": "Summary could not be parsed.",
            "key_points": [],
            "important_concepts": "Concepts could not be parsed."
        }
        
        try:
            # More robust section extraction using markers
            content = response.strip()
            
            # Extract Summary
            if "## Summary" in content:
                summary_part = content.split("## Summary")[1]
                for next_header in ["## Key Points", "## Important Concepts"]:
                    if next_header in summary_part:
                        summary_part = summary_part.split(next_header)[0]
                sections["summary"] = summary_part.strip()
            
            # Extract Key Points
            if "## Key Points" in content:
                points_part = content.split("## Key Points")[1]
                if "## Important Concepts" in points_part:
                    points_part = points_part.split("## Important Concepts")[0]
                
                # Extract bullet points
                for line in points_part.split("\n"):
                    line = line.strip()
                    if line and (line.startswith("-") or line.startswith("*") or line.startswith("•")):
                        # Remove the bullet marker
                        point = re.sub(r'^[\-\*•]\s*', '', line)
                        if point:
                            sections["key_points"].append(point)
            
            # Extract Important Concepts
            if "## Important Concepts" in content:
                concepts_part = content.split("## Important Concepts")[1].strip()
                sections["important_concepts"] = concepts_part
                
            # Fallback if everything failed but we have a response
            if not sections["summary"] or sections["summary"] == "Summary could not be parsed.":
                if not sections["key_points"] and not sections["important_concepts"]:
                    sections["summary"] = response
        
        except Exception as e:
            logger.warning(f"Error parsing response structure: {str(e)}")
            sections["summary"] = response
        
        return sections
