from rag_pipeline import retrieve_context


query = "How many annual leave days does an employee get?"

context = retrieve_context(
    query,
    top_k=3
)

print("\nRetrieved Context:")
print("=" * 60)
print(context)