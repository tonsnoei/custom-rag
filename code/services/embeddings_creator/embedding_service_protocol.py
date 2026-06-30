from typing import Protocol


class EmbeddingServiceProtocol(Protocol):
    def create(self) -> None: ...