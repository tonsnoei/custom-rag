from services.chat.chat_service_protocol import ChatServiceProtocol
from services.vector_repository.vector_repository_protocol import VectorRepositoryProtocol


class LocalLmStudioChatService(ChatServiceProtocol):
    """
    Implements a chat with a local LLM
    """
    def __init__(self, vector_repository: VectorRepositoryProtocol) -> None:
        self._server_base_url = "http://127.0.0.1:1234"
        self._embedding_model = "qwen3.6-35b-a3b-mlx"
        self._vector_repository = vector_repository

    def ask(self, question: str) -> str:
        prompt: str = self._create_prompt(question)

    def _create_prompt(self, question: str) -> str:
        # Find info in the vector database about this question
        related_info_chunks: list[str] = self._vector_repository.search(question, 2)


