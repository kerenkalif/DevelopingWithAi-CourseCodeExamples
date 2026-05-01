from llm_strategy import LLMStrategy
from anthropic_strategy import AnthropicStrategy
from openai_strategy import OpenAIStrategy
from gemini_strategy import GeminiStrategy
from ollama_strategy import OllamaStrategy


class LLMClientFactory:

    _registry: dict[str, type[LLMStrategy]] = {
        "anthropic": AnthropicStrategy,
        "openai": OpenAIStrategy,
        "gemini": GeminiStrategy,
        "ollama": OllamaStrategy,
    }

    @staticmethod
    def create(provider: str) -> LLMStrategy:
        provider = provider.lower().strip()

        strategy_class = LLMClientFactory._registry.get(provider)
        if not strategy_class:
            available = ", ".join(LLMClientFactory._registry.keys())
            raise ValueError(f"Unknown provider: '{provider}'. Available: {available}")
        return strategy_class()
