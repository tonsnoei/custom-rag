from typing import Protocol, Optional


class EmbeddingServiceProtocol(Protocol):
    def create(self, text: str) -> Optional[list[float]]: ...