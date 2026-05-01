from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

system_role = input("What role do you wnat the LLM to have? ")
messages = [
    SystemMessage(system_role)
]

while True:
    user_input = input("--> ")
    if user_input == "exit":
        break
    
    messages.append(HumanMessage(user_input))

    full_response = ""
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content

    print() 
    messages.append(AIMessage(full_response))

    
    