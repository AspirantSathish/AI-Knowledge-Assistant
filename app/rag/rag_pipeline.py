from .embeddings import create_embeddings
from .vector_store import create_vector_store, search_documents


def retrieve_context(query,top_k=3,max_distance=0.7):

    collection = create_vector_store()

    # Create embedding for the user's question
    query_embedding = create_embeddings([query])[0]

    # Retrieve relevant chunks
    results = search_documents(
        collection,
        query_embedding,
        top_k=top_k
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []

    sources = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        
        if distance > max_distance:
            continue

        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"""
    [Source: {source}, Page: {page}]

    {document}
    """
        )

        sources.append({
            "source": source,
            "page": page,
            "distance": distance
        })
        

    context = "\n\n".join(context_parts)

    return context, sources