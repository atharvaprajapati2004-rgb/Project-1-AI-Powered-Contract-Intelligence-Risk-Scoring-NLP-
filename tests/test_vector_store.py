from backend.app.embeddings.embedding_generator import embed_contract
from backend.app.vector_store.faiss_store import FAISSVectorStore


contract_1 = """
PAYMENT

The buyer shall make payment within thirty days of receiving the invoice.

TERMINATION

Either party may terminate this agreement by providing written notice.
"""

contract_2 = """
CONFIDENTIALITY

Both parties shall keep all confidential information private.

LIABILITY

The parties agree to unlimited liability for damages.
"""

embedded_1 = embed_contract(contract_1)
embedded_2 = embed_contract(contract_2)

dimension = embedded_1["embedding_dimension"]

store = FAISSVectorStore(dimension)

store.add_embeddings(
    embedded_1["embeddings"],
    embedded_1["chunks"],
    metadata=[
        {"contract_id": "contract_1"}
        for _ in embedded_1["chunks"]
    ],
)

store.add_embeddings(
    embedded_2["embeddings"],
    embedded_2["chunks"],
    metadata=[
        {"contract_id": "contract_2"}
        for _ in embedded_2["chunks"]
    ],
)

query = "When does the buyer need to make payment?"

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
query_embedding = model.encode(
    query,
    normalize_embeddings=True,
).tolist()

results = store.search(query_embedding, top_k=3)

print("FAISS Vector Store Test")
print("=" * 40)
print(f"Stored vectors: {store.count()}")

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print(f"Score: {result['score']:.4f}")
    print(f"Contract: {result['metadata']['contract_id']}")
    print(f"Chunk: {result['chunk'][:200]}")

assert store.count() == len(embedded_1["chunks"]) + len(embedded_2["chunks"])
assert results
assert results[0]["metadata"]["contract_id"] == "contract_1"

print("\nVector store test completed successfully.")