import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent

async def run_with_mcp(user_message: str):
    client = MultiServerMCPClient(
    {
        "weather": {
            "url": "http://localhost:8001/mcp",  # במקום command+args
            "transport": "streamable_http",       # במקום stdio
        }
    }
    )

    tools = await client.get_tools()

    model = ChatAnthropic(model="claude-sonnet-4-6")
    agent = create_agent(model, tools)

    print(f"User: {user_message}\n")
    response = await agent.ainvoke({"messages": user_message})
    print(f"\nLLM: {response['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(run_with_mcp("what's the temperature at my place?"))