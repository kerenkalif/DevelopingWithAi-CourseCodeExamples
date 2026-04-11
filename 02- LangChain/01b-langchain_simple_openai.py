from secret_key import open_ai_key
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = open_ai_key

llm = ChatOpenAI(model="gpt-4o-mini")
user_prompt = input("--> ")
response = llm.invoke(user_prompt)
print(response.content)