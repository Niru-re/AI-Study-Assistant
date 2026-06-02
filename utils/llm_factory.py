"""
LLM Factory Module

Provides a unified interface for Google Gemini API.
"""

import os
from typing import Optional
import logging
import streamlit as st

logger = logging.getLogger(__name__)


class BaseLLMClient:
    """Base interface for LLM clients."""

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError

    def health_check(self) -> dict:
        """Check if the LLM provider is accessible."""
        raise NotImplementedError


class GeminiClient(BaseLLMClient):
    """Google Gemini API client."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        import google.generativeai as genai
        self.api_key = api_key
        self.model = model
        genai.configure(api_key=api_key)
        self.client = genai
        self.model_instance = genai.GenerativeModel(model)

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using Google Gemini."""
        try:
            response = self.model_instance.generate_content(
                prompt,
                generation_config={
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_output_tokens": 4096,
                }
            )
            
            if not response:
                raise Exception("Empty response from Gemini API")
                
            if response.text:
                return response.text.strip()
            
            # Handle potential safety filters or other reasons for no text
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if candidate.finish_reason != 1: # 1 is STOP
                    raise Exception(f"Gemini generation finished with reason: {candidate.finish_reason}")
            
            raise Exception("No response text received from Gemini")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Gemini API error: {error_msg}")
            
            if "API key" in error_msg or "authentication" in error_msg.lower():
                raise Exception("Gemini API authentication error: Please check your GEMINI_API_KEY in Streamlit secrets.")
            elif "quota" in error_msg.lower() or "429" in error_msg:
                raise Exception("Gemini API quota exceeded: Please try again later or check your usage limits.")
            elif "model not found" in error_msg.lower():
                raise Exception(f"Gemini model '{self.model}' not found. Please check the model name.")
            else:
                raise Exception(f"Gemini API error: {error_msg}")

    def health_check(self) -> dict:
        """Check if Gemini API is accessible."""
        try:
            # Simple test with minimal prompt
            response = self.model_instance.generate_content("Ping", generation_config={"max_output_tokens": 5})
            if response.text:
                return {"status": "ok", "provider": "gemini", "model": self.model}
        except Exception as e:
            return {"status": "error", "provider": "gemini", "model": self.model, "error": str(e)}
        return {"status": "error", "provider": "gemini", "model": self.model}


def get_llm_client() -> Optional[BaseLLMClient]:
    """Factory function to get the Gemini LLM client."""

    # Try to get API key from Streamlit secrets first, then environment variables
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except:
        api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("GEMINI_API_KEY not configured")
        return None

    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    
    try:
        return GeminiClient(api_key=api_key, model=model)
    except ImportError:
        logger.error("Missing dependency: google-generativeai. Run 'pip install google-generativeai'")
        return None
    except Exception as e:
        logger.error(f"Error initializing Gemini client: {str(e)}")
        return None
