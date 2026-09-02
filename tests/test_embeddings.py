from backend.app.embeddings.embedding_generator import embed_contract


sample_contract = """
This agreement is between ABC Technologies and XYZ Solutions.
The payment shall be made within thirty days of receiving the invoice.
Either party may terminate the agreement by providing thirty days written notice.
All confidential information exchanged between the parties must remain confidential.
"""


result = embed_contract(sample_contract)


print("Document Embedding Test")
print("=" * 40)
print(f"Model              : {result['model']}")
print(f"Chunk count        : {result['chunk_count']}")
print(f"Embedding dimension: {result['embedding_dimension']}")

for index, chunk in enumerate(result["chunks"], start=1):
    print(f"\nChunk {index}:")
    print(chunk[:150])

print("\nEmbedding generated successfully.")