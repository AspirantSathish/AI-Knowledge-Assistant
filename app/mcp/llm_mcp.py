import asyncio
import json
import os
import sys

from openai import OpenAI
from dotenv import load_dotenv

from mcp import Client, StdioServerParameters


load_dotenv()

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


SERVER_PATH = os.path.join(
    os.path.dirname(__file__),
    "server.py"
)


server = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_PATH]
)


MODEL = "gpt-4o-mini"


async def main():

    question = "What is my current leave balance? My employee ID is EMP001."

    async with Client(server) as mcp_client:

        # -----------------------------------------
        # 1. Discover MCP tools
        # -----------------------------------------

        tool_result = await mcp_client.list_tools()

        print("\nMCP Tools:")
        for tool in tool_result.tools:
            print(f"- {tool.name}")

        # -----------------------------------------
        # 2. Convert MCP tools to OpenAI tools
        # -----------------------------------------

        tools = []

        for tool in tool_result.tools:

            tools.append({
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema
            })

        # -----------------------------------------
        # 3. Ask LLM
        # -----------------------------------------

        response = openai_client.responses.create(
            model=MODEL,
            instructions=(
                "You are an employee assistant. "
                "Use the available tools when you need "
                "current employee information."
            ),
            input=question,
            tools=tools
        )

        print("\nInitial LLM Response:")
        print(response.output)

        # -----------------------------------------
        # 4. Check whether LLM requested a tool
        # -----------------------------------------

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not tool_calls:

            print("\nFinal Answer:")
            print(response.output_text)

            return

        # -----------------------------------------
        # 5. Execute requested MCP tools
        # -----------------------------------------

        tool_outputs = []

        for call in tool_calls:

            print(f"\nLLM requested tool: {call.name}")

            arguments = json.loads(call.arguments)

            print(f"Arguments: {arguments}")

            result = await mcp_client.call_tool(
                call.name,
                arguments
            )

            # Extract MCP text result
            result_text = ""

            for item in result.content:

                if hasattr(item, "text"):
                    result_text += item.text

            print(f"MCP Result: {result_text}")

            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text
            })

        # -----------------------------------------
        # 6. Send tool result back to LLM
        # -----------------------------------------

        final_response = openai_client.responses.create(
            model=MODEL,
            previous_response_id=response.id,
            input=tool_outputs
        )

        # -----------------------------------------
        # 7. Final answer
        # -----------------------------------------

        print("\nFinal Answer:")
        print("=" * 50)
        print(final_response.output_text)


if __name__ == "__main__":
    asyncio.run(main())