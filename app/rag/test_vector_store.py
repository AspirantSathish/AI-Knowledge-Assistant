from document_loader import load_pdf
from chunker import create_chunks
from embeddings import create_embeddings
from vector_store import create_vector_store, add_documents


pdf_path = "../../documents/leave_policy_sample.pdf"
pdf_path = "D:\\Learning_Projects\\AI Knowledge Assistant\\documents\\leave_policy_sample.pdf"
# 1. Load PDF
pages = load_pdf(pdf_path)

# 2. Create chunks
chunks = create_chunks(
    pages,
    chunk_size=500,
    chunk_overlap=50
)

# 3. Create embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = create_embeddings(texts)

# 4. Create vector store
collection = create_vector_store()

# 5. Store chunks + embeddings
add_documents(
    collection,
    chunks,
    embeddings
)

print(f"Stored {len(chunks)} chunks")

print(f"Collection count: {collection.count()}")