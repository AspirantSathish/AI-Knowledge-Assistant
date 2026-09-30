from rag_pipeline import retrieve_context
from generator import generate_answer


question = "How many annual leave days does an employee get?"

context, sources = retrieve_context(
    question,
    top_k=3
)

answer = generate_answer(
    question,
    context
)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print("=" * 60)
print(answer)

print("\nSources:")
print("=" * 60)

for source in sources:

    print(
        f"File: {source['source']} | "
        f"Page: {source['page']} | "
        f"Distance: {source['distance']:.4f}"
    )