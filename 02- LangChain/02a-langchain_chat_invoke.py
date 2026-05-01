from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

system_role = input("What role do you want the LLM to have? ")
messages = [
    SystemMessage(system_role)
]

while True:
    user_input = input("--> ")
    if user_input == "exit":
        break
    
    messages.append(HumanMessage(user_input))
    response = llm.invoke(messages)
    messages.append(AIMessage(response.content))
    
    print("##############################")
    print(response.content)
    print("##############################")