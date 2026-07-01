from dataclasses import dataclass

@dataclass
class VectorDbRecord:
    vector: list[float]
    text: str

class VectorDbProtocol:
    """
    Represents a vector store where text chunks are stored together with their embeddings.
    """
    def search(self, query_vector: list[float], top_k: int) -> list[VectorDbRecord]:
        """
        Search vector store for given query.
        :param query_vector: The vector to search for
        :param top_k: The number of results to return
        :return: a list of matching vectors
        """
        pass

    def add(self, record: VectorDbRecord) -> None:
        """
        Store record in vector store.
        """
        pass


