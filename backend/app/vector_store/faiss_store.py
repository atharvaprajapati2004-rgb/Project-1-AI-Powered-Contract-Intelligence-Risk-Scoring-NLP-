from typing import Dict, List

import faiss
import numpy as np


class FAISSVectorStore:
    """Local vector store for contract embeddings."""

    def __init__(self, dimension: int):
        if dimension <= 0:
            raise ValueError("dimension must be greater than 0")

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks: List[str] = []
        self.metadata: List[Dict] = []

    def add_embeddings(
        self,
        embeddings: List[List[float]],
        chunks: List[str],
        metadata: List[Dict] | None = None,
    ) -> None:
        """Add contract chunk embeddings to the vector store."""

        if not embeddings:
            return

        if len(embeddings) != len(chunks):
            raise ValueError("embeddings and chunks must have the same length")

        vectors = np.asarray(embeddings, dtype="float32")

        if vectors.ndim != 2 or vectors.shape[1] != self.dimension:
            raise ValueError("Embedding dimension does not match vector store")

        faiss.normalize_L2(vectors)
        self.index.add(vectors)

        self.chunks.extend(chunks)

        if metadata is None:
            metadata = [{} for _ in chunks]

        if len(metadata) != len(chunks):
            raise ValueError("metadata and chunks must have the same length")

        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
    ) -> List[Dict]:
        """Return the most similar contract chunks."""

        if not query_embedding or self.index.ntotal == 0:
            return []

        if top_k <= 0:
            return []

        query = np.asarray([query_embedding], dtype="float32")

        if query.shape[1] != self.dimension:
            raise ValueError("Query embedding dimension does not match vector store")

        faiss.normalize_L2(query)

        k = min(top_k, self.index.ntotal)

        scores, indices = self.index.search(query, k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": float(score),
                    "metadata": self.metadata[index],
                }
            )

        return results

    def count(self) -> int:
        """Return the number of stored vectors."""

        return self.index.ntotal