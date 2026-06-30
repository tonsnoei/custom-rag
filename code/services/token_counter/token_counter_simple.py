from services.token_counter.token_counter_protocol import TokenCounterProtocol


class TokenCounterSimple(TokenCounterProtocol):
    """
    Super simple token counter. Just divide the number of characters by a given value.
    """
    def count(self, text: str) -> int:
        return len(text) // 4 # roughly 4 characters per token