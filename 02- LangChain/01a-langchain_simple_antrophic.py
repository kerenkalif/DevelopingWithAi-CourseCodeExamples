from secret_key import anthropic_key
from langchain_anthropic import ChatAnthropic
import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

print(f"Key length: {len(anthropic_key)}")
print(f"Key starts with: {anthropic_key[:10]}")

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
user_prompt = input("--> ")
response = llm.invoke(user_prompt)
print(response.content)