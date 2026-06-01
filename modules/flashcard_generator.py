"""
Flashcard Generator Module

This module generates flashcards from study notes for active learning.
"""

from typing import Dict, List, Any
from utils.ollama_client import OllamaClient
import logging
import re

logger = logging.getLogger(__name__)


class FlashcardGenerator:
    """
    A class to generate flashcards from study notes.
    
    Attributes:
        client (OllamaClient): The Ollama client for API calls
        prompt_template (str): The prompt template for flashcard generation
    """
    
    def __init__(self, client: OllamaClient, prompt_template: str) -> None:
        """
        Initialize the FlashcardGenerator.
        
        Args:
            client: OllamaClient instance for API calls
            prompt_template: Template for the flashcard prompt
        """
        self.client = client
        self.prompt_template = prompt_template
    
    def generate_flashcards(self, notes: str) -> List[Dict[str, str]]:
        """
        Generate flashcards from study notes.
        
        Args:
            notes: The study notes to create flashcards from
        
        Returns:
            List of flashcards with front and back content
        
        Raises:
            Exception: If flashcard generation fails
        """
        if not notes or notes.strip() == "":
            raise ValueError("Notes cannot be empty")
        
        try:
            # Format prompt with notes
            prompt = self.prompt_template.format(notes=notes)
            
            logger.info("Starting flashcard generation")
            response = self.client.generate(prompt, temperature=0.6)
            
            if not response:
                raise Exception("No response from model")
            
            # Parse response
            flashcards = self._parse_flashcards(response)
            logger.info(f"Generated {len(flashcards)} flashcards")
            return flashcards
        
        except Exception as e:
            logger.error(f"Flashcard generation failed: {str(e)}")
            raise
    
    def _parse_flashcards(self, response: str) -> List[Dict[str, str]]:
        """
        Parse the LLM response into structured flashcards.
        
        Args:
            response: The raw response from LLM
        
        Returns:
            List of parsed flashcards
        """
        flashcards = []
        
        try:
            # Split by "Flashcard N:"
            flashcard_blocks = re.split(r"Flashcard \d+:", response)
            
            for block in flashcard_blocks[1:]:  # Skip first empty split
                flashcard = self._parse_single_flashcard(block)
                if flashcard:
                    flashcards.append(flashcard)
        
        except Exception as e:
            logger.warning(f"Error parsing flashcards: {str(e)}")
            return self._fallback_parse()
        
        return flashcards if flashcards else self._fallback_parse()
    
    def _parse_single_flashcard(self, block: str) -> Dict[str, str]:
        """
        Parse a single flashcard block.
        
        Args:
            block: Text block containing one flashcard
        
        Returns:
            Parsed flashcard dictionary or None
        """
        try:
            flashcard = {
                "front": "",
                "back": ""
            }
            
            # Split by Front: and Back:
            lines = block.strip().split("\n")
            
            current_section = None
            current_content = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("Front:"):
                    if current_section == "back":
                        flashcard["back"] = " ".join(current_content).strip()
                    current_section = "front"
                    current_content = [line[6:].strip()]
                elif line.startswith("Back:"):
                    if current_section == "front":
                        flashcard["front"] = " ".join(current_content).strip()
                    current_section = "back"
                    current_content = [line[5:].strip()]
                elif current_section and line:
                    current_content.append(line)
            
            # Add last section
            if current_section == "front":
                flashcard["front"] = " ".join(current_content).strip()
            elif current_section == "back":
                flashcard["back"] = " ".join(current_content).strip()
            
            # Validate flashcard
            if flashcard["front"] and flashcard["back"]:
                return flashcard
        
        except Exception as e:
            logger.debug(f"Error parsing single flashcard: {str(e)}")
        
        return None
    
    def _fallback_parse(self) -> List[Dict[str, str]]:
        """
        Provide fallback flashcards.
        
        Returns:
            List with placeholder flashcard
        """
        return [{
            "front": "Unable to parse flashcards",
            "back": "Please review the generated content manually."
        }]
