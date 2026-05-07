import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from anthropic import Anthropic
import os

client = Anthropic()

GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
REPO = "kalifi-algo-tracer"
github_token = os.environ.get("github_token")

def print_available_tools(tools):
    for tool in tools:
        print(f'# {tool["name"]}: {tool["description"]}')

async def run_with_mcp(user_message: str):
    async with streamablehttp_client(
        GITHUB_MCP_URL,
        headers={"Authorization": f"Bearer {github_token}"}
    ) as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in mcp_tools
            ]

            print("=== Available Tools ===\n")
            print_available_tools(tools)

            print(f"\n=== Running prompt ===\nUser: {user_message}\n")

            messages = [{"role": "user", "content": user_message}]

            while True:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    tools=tools,
                    messages=messages,
                )

                if response.stop_reason == "tool_use":
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            print(f"  -> {block.name}({block.input})")
                            result = await session.call_tool(block.name, block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0].text,
                            })
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": tool_results})

                else:
                    final_text = next(
                        b.text for b in response.content if hasattr(b, "text")
                    )
                    print(f"\nLLM: {final_text}")
                    break


if __name__ == "__main__":
    asyncio.run(run_with_mcp(
        f"List the 5 most urgent open issues in the repository {REPO}"
    ))