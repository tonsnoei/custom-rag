from typing import Optional, Any

import requests
from requests import Response

from services.embeddings_creator.embedding_service_protocol import EmbeddingServiceProtocol
import json

class NomicEmbeddingService(EmbeddingServiceProtocol):
    """
    This service uses nomic embed to create embeddings. It is OpenAI API Compatible. Therefore, you can use LM Studio
    or Ollama running locally.
    For this service a connection to a Local or Cloud LLM runner is necessary. Embedding models are small, so it is
    no problem to run such models locally.
    """
    def __init__(self):
        self._server_base_url = "http://127.0.0.1:1234"
        self._embedding_model = "text-embedding-nomic-embed-text-v1.5"

    def create(self, text: str = "") ->  Optional[list[float]]:
        url = self._get_embed_url()
        payload = self._create_embed_request_payload(text)

        try:
            response: Response = requests.post(url=url, json=payload)
            response.raise_for_status() # HttpError when status >= 400

            return self._get_embeddings(response)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP-error {e.response.status_code}: {e.response.text}")
        except requests.exceptions.ConnectionError:
            print("Cannot connect to LLM server.")
        except requests.exceptions.Timeout:
            print("Request timed out.")
        except requests.exceptions.RequestException as e:
            print(f"Unexpected failure: {e}")

    def _get_embeddings(self, response: Response) -> Optional[list[float]]:
        response_json = response.json()
        data = response_json.get("data", [])
        if not data:
            return None

        embedding_item = data[0]["embedding"]
        if not embedding_item:
            raise KeyError("No embedding found")

        return [float(item) for item in embedding_item]

    def _get_embed_url(self) -> str:
        return f'{self._server_base_url}/v1/embeddings'

    def _create_embed_request_payload(self, text: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self._embedding_model,
            "input": text,
        }
        return payload