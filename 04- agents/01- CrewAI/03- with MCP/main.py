from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

from mcp import StdioServerParameters


servers_params = [
    StdioServerParameters(
    command="python",
    args=["C:\\Users\\user\\OneDrive\\Teaching\\AI-Driven-Programming\\DevelopingWithAI-ForProgrammers-code_examples\\04- agents\\01- CrewAI\\03- with MCP\\mcp_server\\math_mcp_server.py"]),
    
    StdioServerParameters(
        command="python",
        args=["C:\\Users\\user\\OneDrive\\Teaching\\AI-Driven-Programming\\DevelopingWithAI-ForProgrammers-code_examples\\04- agents\\01- CrewAI\\03- with MCP\\mcp_server\\main.py"]
    )
]


with MCPServerAdapter(servers_params) as tools:
    agent = Agent(
        role="Mathematician",
        goal="Perform mathemtical operations",
        backstory="An expert in mathematics, capable of performing complex calculations quickly and accurately.",
        tools=tools,
        verbose=True
    )
    
    task = Task(
        description="Solve the math problem given to you: {problem}",
        expected_output="The correct answer to the math problem using your available tools.",
        agent=agent
    )
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff(inputs={"problem": "What is 4 multiplied by 2?, then tell me what is the origin of the name 'Avi'? in a list."})
    print("Final Result:", result.raw)
        