from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from secret_key import anthropic_key

import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

parser = JsonOutputParser()

messages = []
user_prompt = "Describe a chocolate cake: name, diameter_cm, is_dairy, price. " + parser.get_format_instructions()
print(user_prompt)
messages.append(HumanMessage(user_prompt))

response = llm.invoke(messages)
print(response.content)
print("--------------")

text_from_parser = parser.invoke(response)
print(text_from_parser)
print(f"Name: {text_from_parser['name']}")
print(f"Price: {text_from_parser['price']}")





