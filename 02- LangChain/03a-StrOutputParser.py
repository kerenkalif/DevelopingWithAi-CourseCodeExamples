from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from secret_key import anthropic_key

import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

system_role = input("What role do you wnat the LLM to have? ")
messages = [
    SystemMessage(system_role)
]

while True:
    user_input = input("--> ")
    if user_input == "exit":
        break
    
    messages.append(HumanMessage(user_input))
    response = llm.invoke(messages)

    direct_text = response.content
    
    parser = StrOutputParser()
    text_from_parser = parser.invoke(response)
    
    
    print("##############################")
    print(f"direct_text = {direct_text}")
    print(f"text_from_parser = {text_from_parser}")
    print("##############################")
    messages.append(AIMessage(text_from_parser))