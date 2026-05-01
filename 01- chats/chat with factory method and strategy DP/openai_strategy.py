from openai import OpenAI
from llm_strategy import LLMStrategy, LLMResponse


class OpenAIStrategy(LLMStrategy):

    def __init__(self):
        self.client = OpenAI()
        self.messages = []

    def set_system_role(self, role: str) -> None:
        self.messages = [{"role": "system", "content": role}]

    def send_message(self, user_input: str) -> LLMResponse:
        self.messages.append({"role": "user", "content": user_input})
        resp = self.client.chat.completions.create(model="gpt-4", messages=self.messages)
        reply = resp.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        return LLMResponse(reply, resp.usage.prompt_tokens, resp.usage.completion_tokens)
