import os
import openai

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    max_retries=2
)

MODEL = os.getenv("OPENAI_MODEL")


SYSTEM_PROMPT = """
You are a helpful AI assistant.

Give clear, concise and accurate answers.
If you don't know something, say that you don't know.
"""


def ask_llm(messages: list, max_tokens: int = 300):

    try:

        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=messages,
            max_output_tokens=max_tokens
        )

        if response.status == "incomplete":
            return (
                "I couldn't complete the response within "
                "the configured response limit."
            )

        return response.output_text


    except openai.AuthenticationError:

        return (
            "The AI service authentication failed. "
            "Please contact the administrator."
        )


    except openai.RateLimitError:

        return (
            "The AI service is currently busy. "
            "Please try again shortly."
        )


    except openai.APIConnectionError:

        return (
            "Unable to connect to the AI service. "
            "Please check your connection and try again."
        )


    except openai.APITimeoutError:

        return (
            "The AI service took too long to respond. "
            "Please try again."
        )


    except openai.APIStatusError as e:

        print(
            f"OpenAI API error: "
            f"status={e.status_code}, "
            f"request_id={e.request_id}"
        )

        return (
            "The AI service encountered an error. "
            "Please try again later."
        )


    except openai.APIError as e:

        print(f"OpenAI API error: {e}")

        return (
            "An unexpected AI service error occurred."
        )