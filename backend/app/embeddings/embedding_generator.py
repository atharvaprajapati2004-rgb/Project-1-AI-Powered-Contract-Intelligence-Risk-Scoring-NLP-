from typing import List

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)


def split_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[str]:
    """
    Split contract text into overlapping word-based chunks.

    Args:
        text: Contract text to split.
        chunk_size: Maximum number of words in each chunk.
        overlap: Number of words repeated between consecutive chunks.

    Returns:
        List of text chunks.
    """
    if not isinstance(text, str) or not text.strip():
        return []

    words = text.split()

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size])
        chunks.append(chunk)
        start += step

    return chunks


def generate_embeddings(text_chunks: List[str]) -> List[List[float]]:
    """
    Generate vector embeddings for text chunks.

    Args:
        text_chunks: List of contract text chunks.

    Returns:
        List of embedding vectors.
    """
    if not text_chunks:
        return []

    embeddings = _model.encode(
        text_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.tolist()


def embed_contract(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> dict:
    """
    Split a contract into chunks and generate embeddings.

    Returns:
        Dictionary containing chunks, embeddings, and model information.
    """
    chunks = split_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    embeddings = generate_embeddings(chunks)

    return {
        "model": MODEL_NAME,
        "chunk_count": len(chunks),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "chunks": chunks,
        "embeddings": embeddings,
    }