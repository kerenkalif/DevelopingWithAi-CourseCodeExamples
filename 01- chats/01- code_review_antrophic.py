from secret_key import antropic_key
from anthropic import Anthropic
import sys

client = Anthropic(api_key=antropic_key)

messages = []
with open("role_python_final_code_review.txt", "r", encoding="utf-8") as f:
    role_str = f.read()

file_path = input("Enter path to code file: ").strip()

with open(file_path, "r", encoding="utf-8") as f:
    user_input = f.read()

messages.append({"role": "user", "content": user_input})
resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=1024, messages=messages, system=role_str)
#print(f"Full response structure\n: {resp.to_json()} ")

reply = resp.content[0].text
messages.append({"role": "assistant", "content": reply})
print(f"Anthropic says: {reply} ")


