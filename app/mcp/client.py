import asyncio
import os
import sys

from mcp import Client, StdioServerParameters


SERVER_PATH = os.path.join(
    os.path.dirname(__file__),
    "server.py"
)


server = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_PATH]
)


async def main():

    print(f"Python: {sys.executable}")
    print(f"Server: {SERVER_PATH}")

    async with Client(server) as client:

        print("\nMCP connection established.")

        result = await client.list_tools()

        print("\nAvailable MCP Tools:")
        print("=" * 50)

        for tool in result.tools:

            print(f"\nName: {tool.name}")
            print(f"Description: {tool.description}")
            print(f"Input Schema: {tool.input_schema}")

        

if __name__ == "__main__":
    asyncio.run(main())