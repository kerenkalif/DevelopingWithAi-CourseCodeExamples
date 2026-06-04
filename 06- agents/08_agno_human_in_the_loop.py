# 08- Agno - Human in the Loop (requires_confirmation)
# Library: agno
# What it does: Agent pauses before sending a weather report to customers.
#               User must confirm or cancel before the action is executed.
# pip install agno openai requests rich

import os

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools import tool
from rich.prompt import Prompt

import requests

from emails_tool import send_gmail

# ── Sender + recipient (controlled by us, NOT by the model) ──
SENDER_EMAIL   = "keren.kalif@gmail.com"
# Gmail App Password - not written in the code!
SENDER_PASSKEY = os.environ["GMAIL_APP_PASSWORD_FOR_STOCK_ANALYZER_AGENT"]
RECIPIENT_EMAIL = "keren.kalif@gmail.com"


@tool()
def get_weather(city: str) -> str:
    """Use this tool to get the current weather for a given city."""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url, timeout=5).text


# Agent-facing tool: requires confirmation (the agent pauses before sending).
# The model only decides subject/body — the recipient and the sender
# credentials are injected here, so the agent can't email an arbitrary address.
@tool(requires_confirmation=True)
def email_report(subject: str, body: str) -> str:
    """Email a weather report (to the fixed company mailing list)."""
    return send_gmail(
        RECIPIENT_EMAIL, subject, body,
        sender_email=SENDER_EMAIL,
        sender_name="Weather Agent",
        sender_passkey=SENDER_PASSKEY,
    )


agent = Agent(
    model=Claude(id="claude-sonnet-4-6"),
    tools=[
        get_weather,
        email_report,
    ],
    description="You are a weather report automation agent.",
    instructions=[
        "Get the weather with get_weather, then email a short report using email_report.",
    ],
    markdown=True,
)

# Run the agent
response = agent.run(
    "Get the weather for Tel Aviv and send a report to all customers."
)

# Handle confirmation pause
while response.is_paused:
    for tool_call in response.tools_requiring_confirmation:
        print(f"\nAbout to execute: {tool_call.tool_name}")
        print(f"Arguments: {tool_call.tool_args}")
        answer = Prompt.ask("Do you want to proceed?", choices=["y", "n"], default="n")
        tool_call.confirmed = (answer == "y")

    # Resume after confirmation. Without stream=True this runs synchronously
    # and returns the final result (the confirmed tool actually executes here).
    response = agent.continue_run(run_response=response)
    print(response.content)

print(response.content)
