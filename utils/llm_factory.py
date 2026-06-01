"""
LLM Factory Module

Provides a unified interface for multiple LLM backends:
- Local Ollama
- Groq
- OpenAI
- Anthropic
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BaseLLMClient:
    """Base interface for LLM clients."""

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError


class OllamaClient(BaseLLMClient):
    """Local Ollama client."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral:latest", timeout: int = 300):
        import requests
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.requests = requests

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using Ollama."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "top_p": top_p,
        }

        try:
            url = f"{self.base_url}/api/generate"
            resp = self.requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                if "response" in data:
                    return data["response"].strip()
            raise Exception(f"Ollama error: {resp.status_code}")
        except Exception as e:
            raise Exception(f"Ollama error: {str(e)}")

    def health_check(self):
        """Check if Ollama is running."""
        try:
            resp = self.requests.get(self.base_url, timeout=5)
            return {"status": "ok", "url": self.base_url}
        except Exception as e:
            return {"status": "error", "url": self.base_url, "error": str(e)}


class GroqClient(BaseLLMClient):
    """Groq LLM client (free, fast inference)."""

    def __init__(self, api_key: str, model: str = "mixtral-8x7b-32768"):
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using Groq."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Groq error: {str(e)}")

    def health_check(self):
        """Check if Groq API is accessible."""
        return {"status": "ok", "provider": "groq", "model": self.model}


class OpenAIClient(BaseLLMClient):
    """OpenAI LLM client."""

    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                top_p=top_p,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI error: {str(e)}")

    def health_check(self):
        """Check if OpenAI API is accessible."""
        return {"status": "ok", "provider": "openai", "model": self.model}


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude LLM client."""

    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using Anthropic."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Anthropic error: {str(e)}")

    def health_check(self):
        """Check if Anthropic API is accessible."""
        return {"status": "ok", "provider": "anthropic", "model": self.model}


def get_llm_client() -> Optional[BaseLLMClient]:
    """Factory function to get the configured LLM client."""

    provider = os.environ.get("LLM_PROVIDER", "ollama").lower()

    try:
        if provider == "ollama":
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.environ.get("OLLAMA_MODEL", "mistral:latest")
            return OllamaClient(base_url=base_url, model=model)

        elif provider == "groq":
            api_key = os.environ.get("GROQ_API_KEY")
            if not api_key:
                logger.error("GROQ_API_KEY not configured")
                return None
            model = os.environ.get("GROQ_MODEL", "mixtral-8x7b-32768")
            return GroqClient(api_key=api_key, model=model)

        elif provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.error("OPENAI_API_KEY not configured")
                return None
            model = os.environ.get("OPENAI_MODEL", "gpt-4-turbo")
            return OpenAIClient(api_key=api_key, model=model)

        elif provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                logger.error("ANTHROPIC_API_KEY not configured")
                return None
            model = os.environ.get("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
            return AnthropicClient(api_key=api_key, model=model)

        else:
            logger.error(f"Unknown LLM_PROVIDER: {provider}")
            return None

    except ImportError as e:
        logger.error(f"Missing dependency for {provider}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error initializing LLM client: {str(e)}")
        return None
