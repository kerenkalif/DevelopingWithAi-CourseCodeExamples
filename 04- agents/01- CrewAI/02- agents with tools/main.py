from crewai.tools import BaseTool, tool
from crewai import Agent, Task, Crew, Process
import os

class MyCalcTool(BaseTool):
    name:str = "My Calculator Tool"
    description : str = "Use this tool to perform math operations"
    
    def _run(self, equation: str) -> str:
        return eval(equation)


# @tool("Evalutation math tool")
# def my_calc_tool(equation: str) -> int:
#     """Get the length of a word"""
#     return eval(equation)


math_expression = input("Enter math expression: ")

math_agent = Agent(
    role="Math Master",
    goal="You are able to evaulate math expressions",
    backstory="You are a math genius with a great sense of humor.",
    tools=[MyCalcTool()],
    verbose=True
)

task1 = Task(
    description=f"{math_expression}",
    expected_output="Give full details in bullet points",
    agent=math_agent
)


writer_agnet = Agent(
    role="Writer",
    goal="Craft compelling explanations based on the result of the math equations",
    backstory= """You are renowed content strategist, known for insightful and engaging
                articles. You transform complex concepts into compelling narratives.
                """,
    verbose=True
)

task2 = Task(
 description="""
        Using the insights provided, explain in great detail how the equation
        and result formed.
    """,
    expected_output="""
        Explain in great detail ans save in markdown. Do not add the triple tick marks
        at the beginning or end of the file. Also don't say what type 
    """,
    output_file="math.md",
    agent=writer_agnet
)


crew = Crew(
    agents=[math_agent, writer_agnet],
    tasks=[task1, task2],
    verbose=True,
    process=Process.sequential
)

result = crew.kickoff()
print("#################")
print(result)