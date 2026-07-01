import textwrap
from typing import Any

import requests
from requests import Response

from services.chat.chat_service_protocol import ChatServiceProtocol
from services.vector_repository.vector_repository_protocol import VectorRepositoryProtocol


class LocalLmStudioChatService(ChatServiceProtocol):
    """
    Implements a chat with a local LLM
    """
    def __init__(self, vector_repository: VectorRepositoryProtocol) -> None:
        self._server_base_url = "http://127.0.0.1:1234"
        self._embedding_model = "qwen3.6-35b-a3b-mlx"
        self._context_length = 8000
        self._temperature = 0
        self._vector_repository = vector_repository

    def ask(self, question: str) -> str:
        url = self._get_chat_url()
        user_prompt: str = self._create_prompt(question)
        system_prompt = self._create_system_prompt()
        chat_request_payload = self._build_chat_request_payload(user_prompt, system_prompt)
        try:
            response: Response = requests.post(url=url, json=chat_request_payload)
            response.raise_for_status()  # HttpError when status >= 400

            return self._get_response_content(response)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP-error {e.response.status_code}: {e.response.text}")
        except requests.exceptions.ConnectionError:
            print("Cannot connect to LLM server.")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Unexpected failure: {e}")

    def _get_response_content(self, response: Response) -> str:
        response_json = response.json()
        data = response_json.get("output", [])

        if len(data) == 0:
            raise Exception(f"Empty response from server: {response.text}")

        content_item = data[0].get("content")

        if not content_item:
            raise Exception(f"Empty response from server: {response.text}")

        return content_item

    def _create_prompt(self, question: str) -> str:
        # Find info in the vector database about this question
        related_info_chunks: list[str] = self._vector_repository.search(question, 2)

        double_newline: str = '\n'
        result: str = textwrap.dedent(f"""
        Context:
        {double_newline.join(related_info_chunks)}
        
        Vraag: {question}
        """)

        return result.strip()

    def _create_system_prompt(self) -> str:
        return "Beantwoord de vraag uitsluitend op basis van de gegeven context."
    def _get_chat_url(self) -> str:
        return f"{self._server_base_url}/api/v1/chat"

    def _build_chat_request_payload(self, user_prompt: str, system_prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self._embedding_model,
            "input": user_prompt,
            "system_prompt": system_prompt,
            "context_length": self._context_length,
            "temperature": self._temperature,
        }
        return payload


