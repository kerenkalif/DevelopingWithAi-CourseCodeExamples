import requests
from llm_strategy import LLMStrategy, LLMResponse

OLLAMA_URL = "http://localhost:11434/api/chat"


def _extract_root_cause(error: Exception) -> str:
    msg = str(error)
    if "Connection refused" in msg or "Failed to establish" in msg:
        return "❌ Ollama is not running. Please start Ollama."
    if "timeout" in msg.lower():
        return "⚠️ The local model is taking too long to respond."
    return f"⚠️ Local model error: {msg}"


class OllamaStrategy(LLMStrategy):

    def __init__(self, model: str = "mistral"):
        self.model = model
        self.messages = []

    def set_system_role(self, role: str) -> None:
        self.messages = [{"role": "system", "content": role}]

    def send_message(self, user_input: str) -> LLMResponse:
        self.messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": self.model, "messages": self.messages, "stream": False},
            )

            if response.status_code != 200:
                raise RuntimeError(f"HTTP Error {response.status_code}")

            data = response.json()
            reply = data["message"]["content"]
            self.messages.append({"role": "assistant", "content": reply})

            input_tokens = data.get("prompt_eval_count", 0)
            output_tokens = data.get("eval_count", 0)
            return LLMResponse(reply, input_tokens, output_tokens)

        except Exception as e:
            raise RuntimeError(_extract_root_cause(e)) from e
