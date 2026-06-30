from typing import Optional

from services.chunker.chunker_protocol import ChunkerProtocol
from services.chunker.markdown_chunker_service import MarkDownChunkerService
from services.token_counter.token_counter_protocol import TokenCounterProtocol
from services.token_counter.token_counter_tiktoken import TokenCounterTikToken


class Dependencies:
    _instance: Optional['Dependencies'] = None

    @staticmethod
    def instance() -> 'Dependencies':
        if not Dependencies._instance:
            Dependencies._instance = Dependencies()
        assert Dependencies._instance is not None
        return Dependencies._instance

    def __init__(self):
        self._chunker_service: Optional[ChunkerProtocol] = None
        self._token_counter: Optional[TokenCounterProtocol] = None


    @property
    def chunker_service(self) -> ChunkerProtocol:
        if self._chunker_service is None:
            self._chunker_service = MarkDownChunkerService(self.token_counter)
        assert self._chunker_service is not None
        return self._chunker_service

    @property
    def token_counter(self) -> TokenCounterProtocol:
        if self._token_counter is None:
            self._token_counter = TokenCounterTikToken()
        assert self._token_counter is not None
        return self._token_counter

