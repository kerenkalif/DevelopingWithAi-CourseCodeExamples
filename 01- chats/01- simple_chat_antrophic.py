from secret_key import antropic_key
from anthropic import Anthropic

client = Anthropic(api_key=antropic_key)

messages = []
role_str = input("What role do you want to give the ai? ")

while True:
    user_input = input("Enter your request: ")
    messages.append({"role": "user", "content": user_input})
    resp = client.messages.create(model="claude-sonnet-4-6", max_tokens=1024, messages=messages, system=role_str)
    print(f"Full response structure\n: {resp.to_json()} ")

    reply = resp.content[0].text
    messages.append({"role": "assistant", "content": reply})
    print(f"Anthropic says: {reply} ")

    print(f"Input tokens used so far: {resp.usage.input_tokens} ")
    print(f"Output tokens used so far: {resp.usage.output_tokens} ")
