import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from anthropic import Anthropic

client = Anthropic()

async def run_with_mcp(user_message: str):
    async with streamable_http_client("http://localhost:8001/mcp") as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()

            # 1. Discover tools automatically
            mcp_tools = (await session.list_tools()).tools
            tools = [
                {
                    "name": t.name,
                    "description": t.description,
                    "input_schema": t.inputSchema,
                }
                for t in mcp_tools
            ]
            print(f"User: {user_message}\n")

            messages = [{"role": "user", "content": user_message}]

            # 2. Agentic loop
            while True:
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    tools=tools,
                    messages=messages,
                )

                # 3. If LLM wants to call tools
                if response.stop_reason == "tool_use":
                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":
                            print(f"  -> {block.name}")
                            result = await session.call_tool(block.name, block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0].text,
                            })

                    # Add assistant response + tool results to history
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": tool_results})

                # 4. Final answer
                else:
                    final_text = next(
                        b.text for b in response.content if hasattr(b, "text")
                    )
                    print(f"\nLLM: {final_text}")
                    break


if __name__ == "__main__":
    asyncio.run(run_with_mcp("what's the temperature at my place?"))