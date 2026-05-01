from anthropic import Anthropic
from llm_strategy import LLMStrategy, LLMResponse

class AnthropicStrategy(LLMStrategy):

    def __init__(self):
        self.client = Anthropic()
        self.messages = []
        self.system_role = ""

    def set_system_role(self, role: str) -> None:
        self.system_role = role

    def send_message(self, user_input: str) -> LLMResponse:
        self.messages.append({"role": "user", "content": user_input})
        resp = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=self.messages,
            system=self.system_role,
        )
        reply = resp.content[0].text
        self.messages.append({"role": "assistant", "content": reply})
        return LLMResponse(reply, resp.usage.input_tokens, resp.usage.output_tokens)
