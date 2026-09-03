from backend.app.embeddings.embedding_generator import embed_contract
from backend.app.search.semantic_search import semantic_search


sample_contract = """
PAYMENT

The buyer shall make payment within thirty days of receiving the invoice.

TERMINATION

Either party may terminate this agreement by providing written notice.

CONFIDENTIALITY

Both parties shall keep all confidential information private.

LIABILITY

The parties agree to unlimited liability for damages.
"""


embedded = embed_contract(sample_contract)

results = semantic_search(
    query="When should the buyer make the payment?",
    chunks=embedded["chunks"],
    embeddings=embedded["embeddings"],
    top_k=3,
)


print("Semantic Search Test")
print("=" * 40)

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print(f"Similarity Score: {result['score']:.4f}")
    print(f"Chunk: {result['chunk'][:200]}")

print("\nSemantic search completed successfully.")