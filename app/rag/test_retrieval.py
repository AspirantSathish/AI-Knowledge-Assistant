from embeddings import create_embeddings
from vector_store import create_vector_store, search_documents


query = "How many annual leave days does an employee get?"

# Connect to existing ChromaDB
collection = create_vector_store()

# Create embedding for user question
query_embedding = create_embeddings([query])[0]

# Search vector database
results = search_documents(
    collection,
    query_embedding,
    top_k=3
)

# Display results
for i, document in enumerate(results["documents"][0]):

    print("\n-----------------------------")
    print(f"Result {i + 1}")

    print("\nDocument:")
    print(document)

    print("\nMetadata:")
    print(results["metadatas"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])