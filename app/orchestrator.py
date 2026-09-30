import asyncio
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from mcp import Client, StdioServerParameters

from rag.rag_pipeline import retrieve_context


load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-4o-mini"


SERVER_PATH = os.path.join(
    os.path.dirname(__file__),
    "mcp",
    "server.py"
)


server = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_PATH]
)

async def ask_assistant(question, employee_id):

    async with Client(server) as mcp_client:

        # -----------------------------------------
        # 1. Retrieve RAG context
        # -----------------------------------------

        context, sources = retrieve_context(
            question,
            top_k=3
        )

        # -----------------------------------------
        # 2. Discover MCP tools
        # -----------------------------------------

        mcp_tools = await mcp_client.list_tools()

        tools = []

        for tool in mcp_tools.tools:

            tools.append({
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            })

        # -----------------------------------------
        # 3. Build LLM prompt
        # -----------------------------------------

        prompt = f"""
You are an AI employee assistant.

Use the provided policy context to answer
questions about company policies.

You may use available tools when the user
asks about live employee-specific information.

Policy Context:
----------------
{context}
----------------

Employee ID:
{employee_id}

User Question:
{question}
"""

        # -----------------------------------------
        # 4. Ask LLM
        # -----------------------------------------

        response = openai_client.responses.create(
            model=MODEL,
            instructions="""
Answer accurately using the available information.

Use policy context for company policy questions.

Use MCP tools when employee-specific live data
is required.

Do not invent information.
""",
            input=prompt,
            tools=tools
        )

        # -----------------------------------------
        # 5. Check for MCP tool calls
        # -----------------------------------------

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:

            return {
                "answer": response.output_text,
                "sources": sources
            }

        # -----------------------------------------
        # 6. Execute MCP tools
        # -----------------------------------------

        tool_outputs = []

        for call in tool_calls:

            arguments = json.loads(call.arguments)

            # Safety: make sure employee ID comes
            # from our application context.
            if "employee_id" in arguments:
                arguments["employee_id"] = employee_id

            result = await mcp_client.call_tool(
                call.name,
                arguments
            )

            result_text = ""

            for item in result.content:

                if hasattr(item, "text"):
                    result_text += item.text

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text
            })

        # -----------------------------------------
        # 7. Send MCP result back to LLM
        # -----------------------------------------

        final_response = openai_client.responses.create(
            model=MODEL,
            previous_response_id=response.id,
            input=tool_outputs
        )

        return {
            "answer": final_response.output_text,
            "sources": sources
        }
        
if __name__ == "__main__":

    question = (
        "Can I take 5 days of annual leave, "
        "and how many annual leave days do I "
        "currently have?"
    )

    result = asyncio.run(
        ask_assistant(
            question,
            employee_id="EMP001"
        )
    )

    print("\nAnswer:")
    print("=" * 60)
    print(result["answer"])

    print("\nSources:")
    print("=" * 60)

    for source in result["sources"]:
        print(source)