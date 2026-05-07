import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

def print_available_tools(tools):
    print(tools)
    for tool in tools:
        print("----------")
        print(f'name: {tool.name}')
        print(f'description: {tool.description}')
        print(f'schema: {tool.inputSchema}')
        
async def discover_mcp_tools():
    async with streamable_http_client("http://localhost:8001/mcp") as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            print_available_tools(mcp_tools)
            
if __name__ == "__main__":
    asyncio.run(discover_mcp_tools())