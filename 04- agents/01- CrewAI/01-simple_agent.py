from crewai import Agent, Task, Crew

info_agent = Agent(
    role="Senior AI Python Developer",
    goal="Provide comprehensive technical information about MCP",
    backstory="You have 15 years of Python experience, contributed to open source, "
              "and your colleagues always turn to you with architecture questions. "
              "You have strong opinions about clean code and proper documentation.",
    verbose=True
)

task1 = Task(
    description="Tell me all about MCP: what is it and what does it used for.",
    expected_output="A quick summary with at least 7 bullet points covering "
                    "key features, use cases, and advantages",
    agent=info_agent
)

task2 = Task(
    description="Tell me all about Agents: what is it and what does it used for.",
    expected_output="A quick summary with at least 7 bullet points covering "
                    "key features, use cases, and advantages",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task1, task2],
    verbose=True
)

result = crew.kickoff()
print("###################")
print(result)