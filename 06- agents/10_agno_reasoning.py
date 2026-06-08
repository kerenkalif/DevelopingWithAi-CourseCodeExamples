from anthropic import Anthropic
from agno.agent import Agent
from agno.models.anthropic import Claude

agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    reasoning=True,
    show_full_reasoning=True,
    tools=[
        collect_and_summarize_stocks,
        write_to_log,
        EmailTools(...),
    ],
    instructions=[
        "Analyze stocks.",
        "Send email only for urgent signals.",
    ],
)
