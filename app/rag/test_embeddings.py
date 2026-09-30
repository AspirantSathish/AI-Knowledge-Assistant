from document_loader import load_pdf
from chunker import create_chunks
from embeddings import create_embeddings


pdf_path = "../../documents/leave_policy_sample.pdf"
pdf_path = "D:\\Learning_Projects\\AI Knowledge Assistant\\documents\\leave_policy_sample.pdf"

# Step 1
pages = load_pdf(pdf_path)


# Step 2
chunks = create_chunks(
    pages,
    chunk_size=500,
    chunk_overlap=50
)


# Step 3
texts = [
    chunk["text"]
    for chunk in chunks
]


embeddings = create_embeddings(texts)


print(f"Number of chunks: {len(chunks)}")

print(f"Number of embeddings: {len(embeddings)}")

print(
    f"Embedding dimensions: {len(embeddings[0])}"
)


print("\nFirst embedding:")

print(embeddings[0])