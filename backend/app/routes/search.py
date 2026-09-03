from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.embeddings.embedding_generator import embed_contract
from backend.app.vector_store.faiss_store import FAISSVectorStore
from sentence_transformers import SentenceTransformer


router = APIRouter()

MODEL_NAME = "all-MiniLM-L6-v2"
_model = SentenceTransformer(MODEL_NAME)

# In-memory vector store for the running application.
_store = None


class ContractIndexRequest(BaseModel):
    contract_id: str
    text: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


def _get_store(dimension: int) -> FAISSVectorStore:
    global _store

    if _store is None:
        _store = FAISSVectorStore(dimension)

    return _store


@router.post("/api/search/index")
def index_contract(request: ContractIndexRequest):
    """Index a contract for semantic search."""

    if not request.text.strip():
        return {"message": "Contract text cannot be empty"}

    embedded = embed_contract(request.text)

    store = _get_store(embedded["embedding_dimension"])

    metadata = [
        {"contract_id": request.contract_id}
        for _ in embedded["chunks"]
    ]

    store.add_embeddings(
        embedded["embeddings"],
        embedded["chunks"],
        metadata,
    )

    return {
        "message": "Contract indexed successfully",
        "contract_id": request.contract_id,
        "chunks_indexed": len(embedded["chunks"]),
        "total_vectors": store.count(),
    }


@router.post("/api/search")
def search_contracts(request: SearchRequest):
    """Search indexed contracts using semantic similarity."""

    if not request.query.strip():
        return {
            "query": request.query,
            "results": [],
        }

    if _store is None:
        return {
            "query": request.query,
            "results": [],
            "message": "No contracts have been indexed yet",
        }

    query_embedding = _model.encode(
        request.query,
        normalize_embeddings=True,
    ).tolist()

    results = _store.search(
        query_embedding,
        top_k=request.top_k,
    )

    return {
        "query": request.query,
        "results": results,
        "total_results": len(results),
    }


@router.get("/api/search/stats")
def search_stats():
    """Return vector search store statistics."""

    return {
        "indexed_vectors": 0 if _store is None else _store.count(),
        "status": "ready" if _store is not None else "empty",
    }