"""
Quiz Generator Module

This module generates multiple-choice quizzes from study notes.
"""

from typing import Dict, List, Any
from utils.llm_factory import BaseLLMClient
import logging
import re

logger = logging.getLogger(__name__)


class QuizGenerator:
    """
    A class to generate multiple-choice quizzes from study notes.
    
    Attributes:
        client (BaseLLMClient): The LLM client for API calls
        prompt_template (str): The prompt template for quiz generation
    """
    
    def __init__(self, client: BaseLLMClient, prompt_template: str) -> None:
        """
        Initialize the QuizGenerator.
        
        Args:
            client: BaseLLMClient instance for API calls
            prompt_template: Template for the quiz prompt
        """
        self.client = client
        self.prompt_template = prompt_template
    
    def generate_quiz(self, notes: str) -> List[Dict[str, Any]]:
        """
        Generate a quiz from study notes.
        
        Args:
            notes: The study notes to create quiz from
        
        Returns:
            List of quiz questions with options and answers
        
        Raises:
            Exception: If quiz generation fails (e.g. Gemini API error)
        """
        if not notes or notes.strip() == "":
            raise ValueError("Notes cannot be empty")
        
        try:
            # Format prompt with notes
            prompt = self.prompt_template.format(notes=notes)
            
            logger.info("Starting Gemini quiz generation")
            # Using slightly higher temperature for variety in questions
            response = self.client.generate(prompt, temperature=0.75)
            
            if not response:
                raise Exception("Gemini returned an empty response for the quiz")
            
            # Parse response
            questions = self._parse_questions(response)
            
            if not questions:
                logger.warning("No questions could be parsed from Gemini response")
                return self._fallback_parse(response)
                
            logger.info(f"Generated {len(questions)} questions successfully")
            return questions
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Quiz generation failed: {error_msg}")
            # Re-raise with a bit more context if it's a Gemini error
            if "Gemini" in error_msg:
                raise Exception(f"Gemini Quiz Error: {error_msg}")
            raise
    
    def _parse_questions(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse the LLM response into structured quiz questions.
        
        Args:
            response: The raw response from LLM
        
        Returns:
            List of parsed questions
        """
        questions = []
        
        try:
            # Split by "Question N:"
            question_blocks = re.split(r"Question \d+:", response)
            
            for block in question_blocks[1:]:  # Skip first empty split
                question_data = self._parse_single_question(block)
                if question_data:
                    questions.append(question_data)
        
        except Exception as e:
            logger.warning(f"Error parsing questions: {str(e)}")
            return self._fallback_parse(response)
        
        return questions
    
    def _parse_single_question(self, block: str) -> Dict[str, Any]:
        """
        Parse a single question block.
        
        Args:
            block: Text block containing one question
        
        Returns:
            Parsed question dictionary or None
        """
        try:
            lines = block.strip().split("\n")
            question_dict = {
                "question": "",
                "options": {"A": "", "B": "", "C": "", "D": ""},
                "correct_answer": "",
                "explanation": ""
            }
            
            # Extract question
            if lines:
                question_dict["question"] = lines[0].strip()
            
            # Extract options and answer
            for line in lines[1:]:
                line = line.strip()
                if line.startswith("A)"):
                    question_dict["options"]["A"] = line[2:].strip()
                elif line.startswith("B)"):
                    question_dict["options"]["B"] = line[2:].strip()
                elif line.startswith("C)"):
                    question_dict["options"]["C"] = line[2:].strip()
                elif line.startswith("D)"):
                    question_dict["options"]["D"] = line[2:].strip()
                elif line.startswith("Correct Answer:"):
                    question_dict["correct_answer"] = line.split(":")[-1].strip()
                elif line.startswith("Explanation:"):
                    question_dict["explanation"] = line.split(":", 1)[-1].strip()
            
            # Validate question
            if (question_dict["question"] and 
                any(question_dict["options"].values()) and 
                question_dict["correct_answer"]):
                return question_dict
        
        except Exception as e:
            logger.debug(f"Error parsing single question: {str(e)}")
        
        return None
    
    def _fallback_parse(self, response: str) -> List[Dict[str, Any]]:
        """
        Fallback parsing if structured parsing fails.
        
        Args:
            response: The raw response from LLM
        
        Returns:
            List with raw response
        """
        return [{
            "question": "Unable to parse questions",
            "options": {},
            "correct_answer": "",
            "explanation": response[:500]
        }]
