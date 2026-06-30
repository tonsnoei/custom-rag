import tiktoken

from services.token_counter.token_counter_protocol import TokenCounterProtocol


class TokenCounterTikToken(TokenCounterProtocol):
    """
    Token counter for Tik-Token. This is a rough token counter which can differ from the real tokens with a margin around 15%
    It uses cl100k_base
    """
    def __init__(self):
        # cl100k_base is de naam van OpenAI's BPE-tokenizer encoding die gebruikt wordt door GPT-3.5 en GPT-4
        self._encoding = tiktoken.get_encoding('cl100k_base')

    def count(self, text: str) -> int:
        return len(self._encoding.encode(text))
