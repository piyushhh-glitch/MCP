import asyncio
from fastmcp import Client

MCP_SERVER_URL="http://localhost:8000/mcp"

async def main():
    async with Client(MCP_SERVER_URL) as client:

        tools=await client.list_tools()

        for tool in tools:
            print(tool.name)

        result= await client.call_tool(
            "create_notes",
            {
                "title": "My First MCP Note",
                "content": "Successfully created through my Notion MCP Server!"
            }
        )

        print(result)

asyncio.run(main())