def create_chunks(pages, chunk_size=500, chunk_overlap=50):

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text.strip(),
                    "metadata": {
                        "source": "leave_policy_sample.pdf",
                        "page": page["page"]
                    }
                })

            start += chunk_size - chunk_overlap

    return chunks