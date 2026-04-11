import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3"

messages = []
role_str = input("What role do you want to give the ai? ")
messages.append({"role": "system", "content": role_str})

while True:
    user_input = input("Enter your request: ")
    messages.append({"role": "user", "content": user_input})

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False
        }
    )

    data = response.json()
    reply = data["message"]["content"]
    messages.append({"role": "assistant", "content": reply})

    print(f"Ollama says: {reply}")
    print(f"Tokens used so far: {data['prompt_eval_count']}")