from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
user_prompt = input("--> ")
response = llm.invoke(user_prompt)
print(response.content)