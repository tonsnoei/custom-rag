from typing import Protocol


class ChatServiceProtocol(Protocol):
    def ask(self, question: str) -> str: ...
