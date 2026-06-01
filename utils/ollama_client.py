"""
Ollama Client Module

This module provides utilities to interact with the Ollama API for LLM operations.
It handles connection management, request formatting, and error handling.
"""

import requests
from typing import Optional, Dict, Any, List
import logging
import subprocess
import shutil

logger = logging.getLogger(__name__)


class OllamaClient:
    """Robust client for interacting with Ollama API.

    This client attempts multiple known endpoints and provides detailed
    debug information on failures. It can also check model availability
    via the `ollama` CLI (when available) and optionally pull missing models.
    """

    # Use the official Ollama generation endpoint only
    GENERATE_ENDPOINTS = ["/api/generate"]

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral:latest",
        timeout: int = 300,
        auto_pull: bool = True,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.auto_pull = auto_pull

    def _full_url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text using the first working Ollama endpoint.

        Tries multiple endpoints and returns the model response string.
        Raises Exception with detailed debug information if all endpoints fail.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "top_p": top_p,
        }

        last_error: Optional[Exception] = None
        debug_info: List[Dict[str, Any]] = []

        for endpoint in self.GENERATE_ENDPOINTS:
            url = self._full_url(endpoint)
            try:
                logger.info(f"Trying Ollama endpoint: {url}")
                resp = requests.post(url, json=payload, timeout=self.timeout)
                debug_info.append({"url": url, "status_code": resp.status_code, "body": resp.text})
                if resp.status_code == 200:
                    data = resp.json()
                    if "response" in data:
                        return data["response"].strip() if isinstance(data["response"], str) else str(data["response"]).strip()
                    raise Exception(f"Unexpected response shape: {data}")
                last_error = Exception(f"Status {resp.status_code} for {url}: {resp.text}")
            except requests.exceptions.RequestException as e:
                last_error = e
                debug_info.append({"url": url, "exception": str(e)})
            except ValueError as e:
                last_error = e
                debug_info.append({"url": url, "exception": str(e), "body": resp.text})

        # If we reach here, all endpoints failed
        debug_message = {
            "message": "All endpoints failed",
            "model": self.model,
            "attempts": debug_info,
        }

        # If model might be missing, try to ensure availability
        try:
            available = self.list_models()
            debug_message["available_models"] = available
            if available is not None and self.model not in available and self.auto_pull:
                # attempt to pull model
                pull_result = self._pull_model(self.model)
                debug_message["auto_pull"] = pull_result
        except Exception:
            # ignore errors here, include what we have
            pass

        # raise a detailed exception
        raise Exception(f"API Error: {last_error}\nDebug: {debug_message}")

    def health_check(self) -> Dict[str, Any]:
        """Perform health checks on base URL, tags endpoint, and test actual generation.

        Returns a dict with results for: root, /api/tags, and a test generation attempt.
        """
        results: Dict[str, Any] = {}
        
        # check root
        try:
            r = requests.get(self.base_url, timeout=5)
            results["root"] = {"status_code": r.status_code}
        except Exception as e:
            results["root"] = {"error": str(e)}
            return results  # If root fails, don't continue

        # check tags
        try:
            url = self._full_url("/api/tags")
            r = requests.get(url, timeout=5)
            results["tags"] = {"status_code": r.status_code}
        except Exception as e:
            results["tags"] = {"error": str(e)}

        # Test actual generation (most important check)
        try:
            payload = {
                "model": self.model,
                "prompt": "test",
                "stream": False,
            }
            url = self._full_url("/api/generate")
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                data = r.json()
                results["generate"] = {"status_code": 200, "model": self.model}
            else:
                results["generate"] = {"status_code": r.status_code, "error": r.text[:500]}
        except Exception as e:
            results["generate"] = {"error": str(e)}

        return results

    def list_models(self) -> Optional[List[str]]:
        """Attempt to list models using HTTP tags endpoint first, then fallback to `ollama list` CLI.

        Returns a list of model names or None.
        """
        # Try HTTP first
        try:
            url = self._full_url('/api/tags')
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                # Ollama may return list or dict; try common shapes
                if isinstance(data, dict):
                    # look for 'models' or 'tags'
                    for key in ("models", "tags", "images"):
                        if key in data and isinstance(data[key], list):
                            return [str(x) for x in data[key]]
                    # if dict values are strings
                    return [str(k) for k in data.keys()]
                if isinstance(data, list):
                    return [str(x) for x in data]
        except Exception:
            pass

        # Fallback to CLI if available
        if shutil.which("ollama"):
            try:
                proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
                if proc.returncode == 0:
                    lines = [l.strip() for l in proc.stdout.splitlines() if l.strip()]
                    # lines often contain model names in first column
                    models = []
                    for line in lines:
                        parts = line.split()
                        if parts:
                            models.append(parts[0])
                    return models
            except Exception:
                pass

        return None

    def _pull_model(self, model_name: str) -> Dict[str, Any]:
        """Attempt to pull a model using `ollama pull <model>` if CLI is available.

        Returns a dict with result and output.
        """
        if not shutil.which("ollama"):
            return {"error": "ollama CLI not found"}

        try:
            proc = subprocess.run(["ollama", "pull", model_name], capture_output=True, text=True, timeout=600)
            return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
        except Exception as e:
            return {"error": str(e)}
