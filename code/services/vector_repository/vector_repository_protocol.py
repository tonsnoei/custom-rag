class VectorRepositoryProtocol:
    """
    Responsible for storing and search texts. It is a wrapper above the vector_db, so the programmer never
    have to use the vector_db directly.
    """
    def search(self, query: str, top_k: int) -> list[str]: ...
    def add(self, text: str) -> None: ...