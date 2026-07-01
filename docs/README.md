# Creating a custom RAG

## What is RAG? (In simple terms)

**RAG** stands for **Retrieval-Augmented Generation**. It’s a smart technique that makes AI assistants much more accurate and up-to-date.

Imagine an AI working *without* RAG: it only answers based on what it “learned” during training. That information can be outdated, incorrect, or incomplete.

**With RAG, here’s how it works:**
1. **Retrieval:** When you ask a question, the AI first searches trusted sources (like internal documents, recent news articles, or a knowledge base) for relevant information.
2. **Augmentation:** Those found text snippets are directly added to your original question/prompt.
3. **Generation:** The AI uses both its own training knowledge and the *correct* information from the source to craft an accurate answer.

### ✅ Why is this useful?
- **Up-to-date:** Connects to recent data without needing to retrain the AI.
- **More accurate:** Fewer “made-up” answers (hallucinations), since the AI sticks to the retrieved facts.
- **Secure & private:** You can connect the AI to internal company documents without exposing that data publicly.
- **Verifiable:** The AI can often cite sources, so you can check where the answer came from.

### 🛠️ Where is it used?
Customer service (answering based on manuals), research assistants, legal/medical document analysis, and any system where accurate, up-to-date information is crucial.

In short: **RAG gives the AI a “trusted source” to look up, so it answers smarter and more reliably.**

## Why this project?
I want to learn the inner workings of a RAG. So I made my own RAG in a few hours/days. It was fun and I learned a lot. 

## Main Steps
Below you will find an overview of how implemented this custom RAG. There are several steps. I described it in the order I build this project:

1. **Determine supported document types** - Determine what kind of documents to use. I decided to use markdown because it is a common standard with a basic understandable structure
2. **Create a text chunker** - To make the RAG work, larger texts must be split up in smaller parts. There are several methodologies. I used methodology 1 and 2 from [this document](./chunking/chunking-methodologies.md). This is implemented in [MarkDownChunkerService](../code/services/chunker/markdown_chunker_service.py)
3. **Create a token counter** - Text chunks must be limited to a specific size, between 300-500 tokens. However, tokens are not the same as characters. We need to determine the token size of a text. In other words convert a number of characters to a number of tokens. This is done in the token_counter service ([TokenCounterSimple](../code/services/token_counter/token_counter_simple.py), [TokenCounterTikToken](../code/services/token_counter/token_counter_tiktoken.py)). Which of the 2 is used is determined in the [Dependencies](../code/dependencies.py), change it there.
4. **Create embeddings** - An embedding is a vector: an array of float values. With the chunked texts we are ready to create an embedding for each chunk. Embeddings are created with an embedding AI model. We put in text and the output is an array of floats. For this step a host is needed for creating the embeddings. This can be done using a local Ollama or LM Studio. See the configuration section below. The service [NomicEmbeddingService](../code/services/embeddings_creator/nomic_embedding_service.py) is responsible for creating embeddings from text.
5. **Create a vector db and repository** - The embeddings must be stored together with the related texts in a data store, a vector database. An in-memory vector [db](../code/services//vector_db/in_memory_vector_db.py) and [repository](../code/services/vector_repository/nomic_embed_vector_repository.py) is part of the solution. The `add` method makes it possible to add new embeddings. The `search` method implements the essential cosine similarity search. We use `numpy`. The repository is implemented as a wrapper because for nomic embed it is important to prefix documents with `document_search: ` and when a search is performed, the prefix: `document_query: ` must be added. Now, without the next steps you can perform a perfect similarity search and find text chunks that are related to a given question.
6. **Chat Service** - We need a service that answer questions and take the stored documents in account. This service will use an Large Language Model


## Configuration
### Using local LLM Runner
A local LLM runner is a tool like [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai) that can download open weight models from the internet and run it locally.

### Chunk sizes
The size of chunks created can be configured in the `init` method of the [MarkDownChunkerService](../code/services/chunker/markdown_chunker_service.py). The `size` and `overlap` is in tokens (roughly 4 characters per token). Overlap is used when paragraphs are too large and must be split. The overlap will take the overlap amount of tokens of the previous chunk and make it part of the current to ensure a relation between the chunks is maintained.

### Embedding Configuration
The configuration of the [NomicEmbeddingService](../code/services/embeddings_creator/nomic_embedding_service.py) can be changed in the `init` method. It contains the configuration when using a locally running LM Studio. It works for other tools as long as it has an OpenAI compatible API.

### Services
We use Dependency Inversion (DI) as part of the 'D' of the SOLID principle. It also helps with the 'O', Open/Closed principle (open for extension, closed for modification). For each service a protocol is defined. This protocol defines the methods available. Every service is build according to the related procotol. This makes it easy to replace a service with another implementation. Think of the [InMemoryVectorStore](../code/services/vector_store/in_memory_vector_store.py), create a new Store with ChromaDB for example, modify [Dependencies](../code/dependencies.py) (which acts as a Service Locator) to use this store instead. Same for the TokenCounter or Embeddings services.


## AI Use
Yes, I did use the Claude Coding Agent for explaining RAG to me. However, nothing of the code in this repository is generated with AI. It is fully hand written. However, the sample documents ([novalink-x1.md](../code/test-docs/novalink-x1.md), [terraglide-r7](../code/test-docs/terraglide-r7.md)) are generated with AI. 