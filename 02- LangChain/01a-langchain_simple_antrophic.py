from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
user_prompt = input("--> ")
response = llm.invoke(user_prompt)
print(response.content)