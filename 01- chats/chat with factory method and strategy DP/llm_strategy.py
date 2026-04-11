from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    reply: str
    input_tokens: int
    output_tokens: int


class LLMStrategy(ABC):

    @abstractmethod
    def set_system_role(self, role: str) -> None:
        pass

    @abstractmethod
    def send_message(self, user_input: str) -> LLMResponse:
        pass
