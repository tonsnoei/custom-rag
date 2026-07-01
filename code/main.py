# This is a sample Python script.
import textwrap
from typing import Optional

from dependencies import Dependencies

def create_chunks_from_md(text: str, subject: str) -> list[str]:
    """
    Create chunks for a given markdown text
    :param text:
    :param subject:
    :return:
    """
    return Dependencies.instance().chunker_service.create(text, "Test")

def create_embeddings(text: str) -> Optional[list[float]]:
    return Dependencies.instance().embedding_service.create(text)

if __name__ == '__main__':
    text = textwrap.dedent("""
      # Hoofdstuk 1
      Wat introductietekst.

      ## Sectie 1.1
      Inhoud van sectie 1.1.

      ## Sectie 1.2
      Inhoud van sectie 1.2.
      """)
    print(create_chunks_from_md(text, "Test"))
    print(create_embeddings(text))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
