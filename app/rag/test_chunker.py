from document_loader import load_pdf
from chunker import create_chunks


pdf_path = "D:\\Learning_Projects\\AI Knowledge Assistant\\documents\\leave_policy_sample.pdf"


pages = load_pdf(pdf_path)


chunks = create_chunks(
    pages,
    chunk_size=200,
    chunk_overlap=30
)


print(f"Total chunks: {len(chunks)}")


for index, chunk in enumerate(chunks):

    print("\n" + "=" * 60)

    print(f"Chunk {index + 1}")

    print(f"Source: {chunk['metadata']['source']}")

    print(f"Page: {chunk['metadata']['page']}")

    print("-" * 60)

    print(chunk["text"])