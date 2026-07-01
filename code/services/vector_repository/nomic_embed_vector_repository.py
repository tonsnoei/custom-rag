from typing import Optional

from services.embeddings_creator.embedding_service_protocol import EmbeddingServiceProtocol
from services.vector_repository.vector_repository_protocol import VectorRepositoryProtocol
from services.vector_db.vector_db_protocol import VectorDbProtocol, VectorDbRecord


class NomicEmbedVectorRepository(VectorRepositoryProtocol):
    def __init__(self, vector_db: VectorDbProtocol, embedding_service: EmbeddingServiceProtocol) -> None:
        self._vector_db = vector_db
        self._embedding_service = embedding_service

        # nomic-embed-text-v1.5 vereist specifieke prefixes om te weten of het een document of een zoekopdracht verwerkt:
        #
        #   - Chunks opslaan → prefix met search_document:
        #   - Query zoeken → prefix met search_query:
        self._query_prefix = 'search_query: '
        self._document_prefix = 'search_document: '

    def search(self, query: str, top_k: int) -> list[str]:
        vector: Optional[list[float]] = self._embedding_service.create(f'{self._query_prefix}{query}')

        if not vector:
            return []

        records: list[VectorDbRecord] = self._vector_db.search(vector, top_k)
        return [item.text for item in records]

    def add(self, text_chunk: str) -> None:
        final_text = f'{self._document_prefix}{text_chunk}'
        vector: Optional[list[float ]] = self._embedding_service.create(final_text)
        if not vector:
            raise Exception(f'No vector found for {final_text}')
        self._vector_db.add(VectorDbRecord(vector=vector, text=final_text))


