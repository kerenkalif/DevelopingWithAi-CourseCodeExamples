from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from secret_key import anthropic_key

import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

messages = []
messages.append(HumanMessage("Describe a chocolate cake. Return JSON with: name, diameter_cm, is_dairy, price"))

response = llm.invoke(messages)

parser = JsonOutputParser()
text_from_parser = parser.invoke(response)
print(text_from_parser)
print(type(text_from_parser['is_dairy']))
print(type(text_from_parser['diameter_cm']))
print(type(text_from_parser['price']))
