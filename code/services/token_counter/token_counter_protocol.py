from typing import Protocol


class TokenCounterProtocol(Protocol):
    """
    A service responsible for counting how many tokens a text contains
    """
    def count(self, text: str) -> int:
        """
        Counts the number of tokens in a given text
        :param text: The text to count the number of tokens of
        :return: The number of tokens
        """
        pass