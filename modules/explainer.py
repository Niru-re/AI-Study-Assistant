"""
Explainer Module

This module provides functionality to explain topics comprehensively.
"""

from typing import Dict, Any
from utils.ollama_client import OllamaClient
import logging

logger = logging.getLogger(__name__)


class Explainer:
    """
    A class to explain topics using LLM.
    
    Attributes:
        client (OllamaClient): The Ollama client for API calls
        prompt_template (str): The prompt template for explanations
    """
    
    def __init__(self, client: OllamaClient, prompt_template: str) -> None:
        """
        Initialize the Explainer.
        
        Args:
            client: OllamaClient instance for API calls
            prompt_template: Template for the explanation prompt
        """
        self.client = client
        self.prompt_template = prompt_template
    
    def explain(self, topic: str) -> Dict[str, Any]:
        """
        Explain a topic comprehensively.
        
        Args:
            topic: The topic to explain
        
        Returns:
            Dictionary containing definition, concepts, examples, points, and applications
        
        Raises:
            Exception: If explanation fails
        """
        if not topic or topic.strip() == "":
            raise ValueError("Topic cannot be empty")
        
        try:
            # Format prompt with topic
            prompt = self.prompt_template.format(topic=topic)
            
            logger.info(f"Starting explanation for topic: {topic}")
            response = self.client.generate(prompt, temperature=0.6)
            
            if not response:
                raise Exception("No response from model")
            
            # Parse response
            result = self._parse_response(response)
            logger.info("Explanation completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Explanation failed: {str(e)}")
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
            "definition": "",
            "key_concepts": [],
            "examples": [],
            "important_points": [],
            "real_world_applications": []
        }
        
        try:
            # Split by section headers
            current_section = None
            current_content = []
            
            for line in response.split("\n"):
                line_stripped = line.strip()
                
                if "## Definition" in line:
                    current_section = "definition"
                    current_content = []
                elif "## Key Concepts" in line:
                    sections["definition"] = "\n".join(current_content).strip()
                    current_section = "key_concepts"
                    current_content = []
                elif "## Examples" in line:
                    if current_section == "key_concepts":
                        sections["key_concepts"] = self._extract_items(current_content)
                    current_section = "examples"
                    current_content = []
                elif "## Important Points" in line:
                    if current_section == "examples":
                        sections["examples"] = self._extract_items(current_content)
                    current_section = "important_points"
                    current_content = []
                elif "## Real-World Applications" in line:
                    if current_section == "important_points":
                        sections["important_points"] = self._extract_items(current_content)
                    current_section = "applications"
                    current_content = []
                elif current_section and line_stripped:
                    current_content.append(line_stripped)
            
            # Process last section
            if current_section == "definition":
                sections["definition"] = "\n".join(current_content).strip()
            elif current_section == "key_concepts":
                sections["key_concepts"] = self._extract_items(current_content)
            elif current_section == "examples":
                sections["examples"] = self._extract_items(current_content)
            elif current_section == "important_points":
                sections["important_points"] = self._extract_items(current_content)
            elif current_section == "applications":
                sections["real_world_applications"] = self._extract_items(current_content)
        
        except Exception as e:
            logger.warning(f"Error parsing response structure: {str(e)}")
            sections["definition"] = response
        
        return sections
    
    @staticmethod
    def _extract_items(content: list) -> list:
        """
        Extract list items from content lines.
        
        Args:
            content: List of content lines
        
        Returns:
            List of extracted items
        """
        items = []
        for line in content:
            # Remove bullet points and numbering
            if line.startswith("-") or line.startswith("•"):
                items.append(line[1:].strip())
            elif line and line[0].isdigit() and "." in line[:3]:
                # Handle numbered lists like "1. Item"
                items.append(line.split(".", 1)[1].strip())
            elif line:
                items.append(line)
        return items
