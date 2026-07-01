from dataclasses import dataclass
from typing import Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from markdown_it.token import Token

from services.chunker.chunker_protocol import ChunkerProtocol
from markdown_it import MarkdownIt
from markdown_it.tree import SyntaxTreeNode

from services.token_counter.token_counter_protocol import TokenCounterProtocol

class ContextStack:
    """
    ContextStack is used to store the context hierarchy. Think of a document with multiple sub-sections. The
    hierarchy of H1 -> H2 -> H3 -> H4 etc... is stored here. This makes the context more clear for the RAG.
    """
    def __init__(self):
        self._stack: list[str] = []

    def get_stack(self) -> list[str]:
        return self._stack

    def push_smart(self, text: str = "", level: int = 0) -> None:
        while len(self._stack) > level and not len(self._stack) == 0:
            self.pop()
        self._push(text)

    def _push(self, value: str) -> None:
        """
        Add an item to the stack
        :param value:
        :return:
        """
        self._stack.append(value)

    def pop(self) -> None:
        """
        Remove an item from the stack
        :return:
        """
        if len(self._stack) == 0:
            return

        self._stack.pop()


class MarkDownChunkerService(ChunkerProtocol):
    def __init__(self, token_counter: TokenCounterProtocol):
        self._token_counter = token_counter

        # Chunks will not be larger than this number of tokens.
        self._chunk_size: int = 400

        # Larger chunks will be split and have an overlap of the number of tokens below
        self._chunk_overlap: int = 50

    def create(self, data: str, subject: Optional[str]) -> list[str]:
        """
        This function chunks
        :param data: Markdown string
        :return: Chunks
        """
        result: list[str] = []

        md = MarkdownIt()
        md_tokens: list[Token] = md.parse(data)
        md_tree = SyntaxTreeNode(md_tokens)

        context_stack: ContextStack = ContextStack()

        if not subject:
            subject = ''
        context_stack.push_smart(subject, level=0)

        for node in md_tree:
            # print(node.type, node.tag)
            if node.type == 'heading':
                self.add_heading_to_context(context_stack, node)
            elif node.type == 'paragraph':
                result += self.create_chunks(node.children[0].content, context_stack)
            else:
                raise Exception(f"Unsupported node type: {node.type}")

        return result


    def create_chunks(self, data: str, context_stack: ContextStack) -> list[str]:
        context_description = self.create_context_description(context_stack)
        desc_token_count = self._token_counter.count(context_description)
        splitter = RecursiveCharacterTextSplitter(chunk_size=self._chunk_size,
                                                  chunk_overlap=self._chunk_overlap,
                                                  length_function=lambda text: self._token_counter.count(text) - desc_token_count)

        return [f'{context_description} {item}' for item in splitter.split_text(data)]

    def create_context_description(self, context_stack: "ContextStack") -> str:
        """
        Creates a context description. It can be used to add to a chunk
        :param context_stack:
        :return:
        """
        stack = context_stack.get_stack()
        result: str = f'This text fragment is part of "{stack[0]}"'
        if len(stack) > 1:
            result += f', sectie: '
        result += (f', sub-section: '.join(stack[1:]))
        result += '.'
        return result


    def add_heading_to_context(self, context_stack: "ContextStack", node: SyntaxTreeNode) -> None:
        if not node.type == 'heading':
            raise Exception(f"Not a heading: {node}")

        context_stack.push_smart(node.children[0].content, self.get_heading_number(node.tag))


    def get_heading_number(self, tag: str) -> int:
        if len(tag) < 2:
            raise Exception(f"Tag {tag} is too short")

        return int(tag[1])



