import os
from abc import ABC, abstractmethod
from anthropic import Anthropic
import google.generativeai as genai

class LLMProvider(ABC):
    @abstractmethod
    def generate_code(self, system_prompt: str, user_prompt: str) -> str:
        pass

class AnthropicProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada no backend.")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20240620"

    def generate_code(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text

class GeminiProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada no backend.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro-latest")

    def generate_code(self, system_prompt: str, user_prompt: str) -> str:
        # Gemini handles system instructions in model instantiation or by combining with user prompt
        # For simplicity with current SDK, we combine them
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        response = self.model.generate_content(full_prompt)
        return response.text

class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str) -> LLMProvider:
        provider_name = provider_name.lower().strip()
        if provider_name == "anthropic":
            return AnthropicProvider()
        elif provider_name == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Provedor LLM desconhecido: {provider_name}")
