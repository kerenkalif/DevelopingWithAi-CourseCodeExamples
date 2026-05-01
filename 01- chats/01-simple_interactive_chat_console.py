from openai import OpenAI

client = OpenAI()

messages = []
role_str = input("What role do you want to give the ai? ")
messages.append({"role": "system", "content": role_str})
resp = client.chat.completions.create(model="gpt-4", messages=messages)
print(f"Full response structure\n: {resp.to_json()} ")

while True:
    user_input = input("Enter your request: ")
    messages.append({"role": "user", "content": user_input})
    resp = client.chat.completions.create(model="gpt-4", messages=messages)
    reply = resp.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print(f"ChatGPT says: {reply} ")
    print(f"Tokens used so far: {resp.usage.prompt_tokens} ")
