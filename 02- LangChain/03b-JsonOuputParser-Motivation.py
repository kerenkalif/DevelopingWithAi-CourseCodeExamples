from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from secret_key import anthropic_key

import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

messages = []
messages.append(HumanMessage("Describe a chocolate cake. Include in your answer the name of the cake, diameter in cm, if it' dairy, and the price"))

response = llm.invoke(messages)
print(response.content)

