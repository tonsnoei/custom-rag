from services.vector_db.vector_db_protocol import VectorDbProtocol, VectorDbRecord
import numpy as np

class InMemoryVectorDb(VectorDbProtocol):
    def __init__(self):
        self._vectors: list[VectorDbRecord] = []

    def search(self, query_vector: list[float], top_k: int) -> list[VectorDbRecord]:
        """
        :param query_vector:
        :param top_k:
        :return:
        """

        """
        Cosine similarity meet de hoek tussen twee vectors, niet de afstand. Hoe kleiner de hoek, hoe meer ze op elkaar lijken.
        
        De formule:

        similarity = (A · B) / (|A| * |B|)
        
        - A · B — dot product: vermenigvuldig elk element paarsgewijs en tel op
        - |A| en |B| — de lengte (magnitude) van elke vector
        
        Resultaat: altijd tussen -1 en 1. Bij embeddings in de praktijk tussen 0 en 1 — hoe dichter bij 1, hoe relevanter.
        
        Concreet voorbeeld met kleine vectors:
        A = [1, 0, 1]  # embedding van query
        B = [1, 0, 0]  # embedding van een chunk
        
        dot = 1*1 + 0*0 + 1*0  # = 1
        |A| = sqrt(1² + 0² + 1²)  # = 1.41
        |B| = sqrt(1² + 0² + 0²)  # = 1.0
        
        similarity = 1 / (1.41 * 1.0)  # = 0.71
        """
        query = np.array(query_vector)

        scores = []
        for record in self._vectors:
            vector = np.array(record.vector, dtype=np.float64)
            similarity = np.dot(query, vector) / (np.linalg.norm(query) * np.linalg.norm(vector))
            scores.append((similarity, record))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [record for _, record in scores[:top_k]]

    def add(self, record: VectorDbRecord) -> None:
        self._vectors.append(record)