from typing import Optional

from services.chat.chat_service_protocol import ChatServiceProtocol
from services.chat.local_lmstudio_chat_service import LocalLmStudioChatService
from services.chunker.chunker_protocol import ChunkerProtocol
from services.chunker.markdown_chunker_service import MarkDownChunkerService
from services.embeddings_creator.embedding_service_protocol import EmbeddingServiceProtocol
from services.embeddings_creator.nomic_embedding_service import NomicEmbeddingService
from services.vector_repository.nomic_embed_vector_repository import NomicEmbedVectorRepository
from services.vector_repository.vector_repository_protocol import VectorRepositoryProtocol
from services.token_counter.token_counter_protocol import TokenCounterProtocol
from services.token_counter.token_counter_tiktoken import TokenCounterTikToken
from services.vector_db.in_memory_vector_db import InMemoryVectorDb
from services.vector_db.vector_db_protocol import VectorDbProtocol


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
        self._embedding_service: Optional[EmbeddingServiceProtocol] = None
        self._vector_db: Optional[VectorDbProtocol] = None
        self._vector_repository: Optional[VectorRepositoryProtocol] = None
        self._chat_service: Optional[ChatServiceProtocol] = None


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

    @property
    def embedding_service(self) -> EmbeddingServiceProtocol:
        if self._embedding_service is None:
            self._embedding_service = NomicEmbeddingService()
        assert self._embedding_service is not None
        return self._embedding_service

    @property
    def vector_db(self) -> VectorDbProtocol:
        if self._vector_db is None:
            self._vector_db = InMemoryVectorDb()
        assert self._vector_db is not None
        return self._vector_db

    @property
    def vector_repository(self) -> VectorRepositoryProtocol:
        if self._vector_repository is None:
            self._vector_repository = NomicEmbedVectorRepository(self.vector_db, self.embedding_service)
        assert self._vector_repository is not None
        return self._vector_repository

    @property
    def chat_service(self) -> ChatServiceProtocol:
        if self._chat_service is None:
            self._chat_service = LocalLmStudioChatService(self.vector_repository)
        assert self._chat_service is not None
        return self._chat_service



