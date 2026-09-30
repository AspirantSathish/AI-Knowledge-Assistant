import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_answer(question, context):

    instructions = """
You are a helpful company policy assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not make up information.
"""

    prompt = f"""
Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions=instructions,
        input=prompt,
        max_output_tokens=200
    )

    return response.output_text