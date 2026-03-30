from abc import ABC, abstractmethod
import os
import sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ===============================
# 🎯 Strategy
# ===============================
class LLMProvider(ABC):
    @abstractmethod
    def send_message(self, messages, role):
        pass


# ===============================
# 🟢 OpenAI
# ===============================
class OpenAIProvider(LLMProvider):
    def __init__(self):
        from secret_key import open_ai_key
        from openai import OpenAI

        self.client = OpenAI(api_key=open_ai_key)
        self.model = "gpt-4"

    def send_message(self, messages, role):
        request_messages = [{"role": "system", "content": role}] + messages

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=request_messages
        )

        reply = resp.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


# ===============================
# 🟣 Anthropic / Claude
# ===============================
class AnthropicProvider(LLMProvider):
    def __init__(self):
        from secret_key import antropic_key
        from anthropic import Anthropic

        self.client = Anthropic(api_key=antropic_key)
        self.model = "claude-sonnet-4-6"

    def send_message(self, messages, role):
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=messages,
            system=role
        )

        reply = resp.content[0].text
        messages.append({"role": "assistant", "content": reply})
        return reply


# ===============================
# 🔵 Gemini
# ===============================
class GeminiProvider(LLMProvider):
    def __init__(self):
        from secret_key import gemini_key
        from google import genai

        self.client = genai.Client(api_key=gemini_key)
        self.model = "gemini-2.0-flash"

    def send_message(self, messages, role):
        history = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )

        prompt = f"""System role:
{role}

Conversation:
{history}

Assistant:"""

        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        reply = resp.text
        messages.append({"role": "assistant", "content": reply})
        return reply


# ===============================
# 🟠 Ollama
# ===============================
class OllamaProvider(LLMProvider):
    def __init__(self):
        self.model = "llama3"
        self.url = "http://localhost:11434/api/generate"

    def send_message(self, messages, role):
        history = "\n".join(
            f"{m['role']}: {m['content']}" for m in messages
        )

        prompt = f"""System role:
{role}

Conversation:
{history}

Assistant:"""

        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3  
                }
            }
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama HTTP error: {response.status_code} - {response.text}")

        reply = response.json()["response"]
        messages.append({"role": "assistant", "content": reply})
        return reply


# ===============================
# 🏭 Factory
# ===============================
class ProviderFactory:
    @staticmethod
    def create(name: str) -> LLMProvider:
        name = name.lower()

        if name == "openai":
            return OpenAIProvider()
        if name == "claude":
            return AnthropicProvider()
        if name == "gemini":
            return GeminiProvider()
        if name == "ollama":
            return OllamaProvider()

        raise ValueError(f"Unknown provider: {name}")


# ===============================
# 🚀 Main
# ===============================
def main():
    provider_name = input("Choose provider (openai / claude / gemini / ollama): ").strip().lower()
    provider = ProviderFactory.create(provider_name)

    role = input("What role do you want to give the AI? ").strip()

    messages = []

    while True:
        user_input = input("Enter your request (or END): ").strip()

        if user_input == "END":
            print("Bye 👋")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            reply = provider.send_message(messages, role)
            print(f"\nAI says:\n{reply}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()