from typing import Any, Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

_model = SentenceTransformer(MODEL_NAME)


def semantic_search(
    query: str,
    chunks: List[str],
    embeddings: List[List[float]],
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """
    Find the most semantically similar contract chunks for a query.

    Args:
        query: Search query.
        chunks: Contract text chunks.
        embeddings: Pre-generated embeddings for the chunks.
        top_k: Number of results to return.

    Returns:
        Ranked list containing matching chunks and similarity scores.
    """

    if not isinstance(query, str) or not query.strip():
        return []

    if not chunks or not embeddings:
        return []

    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    if top_k <= 0:
        return []

    query_embedding = _model.encode(
        [query],
        normalize_embeddings=True,
    )[0]

    embedding_matrix = np.asarray(embeddings, dtype=float)

    norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1

    normalized_embeddings = embedding_matrix / norms

    scores = normalized_embeddings @ query_embedding

    ranked_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in ranked_indices:
        results.append(
            {
                "chunk": chunks[index],
                "score": float(scores[index]),
            }
        )

    return results