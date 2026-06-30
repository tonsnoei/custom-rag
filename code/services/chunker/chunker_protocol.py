from typing import Protocol, Optional


class ChunkerProtocol(Protocol):
    def create(self, data: str, subject: Optional[str]) -> list[str]:
        """
        Create chunks from given data
        :param data: Textual data to be chunked
        :param subject: Optional subject which describes the given data (e.g. a file name)
        :return: Textual chunks
        """
        pass