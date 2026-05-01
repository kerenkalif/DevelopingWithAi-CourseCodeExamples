from google import genai
from google.genai import types
from llm_strategy import LLMStrategy, LLMResponse

class GeminiStrategy(LLMStrategy):
    def __init__(self):
        self.client = genai.Client()
        self.model = "gemini-2.5-flash"
        self.chat = None
    def set_system_role(self, role: str) -> None:
        self.chat = self.client.chats.create(
            model = self.model,
            config = types.GenerateContentConfig(system_instruction=role),
        )
    def send_message(self, user_input: str) -> LLMResponse:
        resp = self.chat.send_message(user_input)
        input_tokens = resp.usage_metadata.prompt_token_count if resp.usage_metadata else 0
        output_tokens = resp.usage_metadata.candidates_token_count if resp.usage_metadata else 0
        return LLMResponse(resp.text, input_tokens, output_tokens)
