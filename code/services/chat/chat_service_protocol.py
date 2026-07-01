from dataclasses import dataclass
from typing import Protocol


class ChatServiceProtocol(Protocol):
    def ask(self, question: str) -> str: ...

@dataclass
class ChatResponse:
    answer: str # llm answer
    references: list[str] # list of found chunks in the vector database