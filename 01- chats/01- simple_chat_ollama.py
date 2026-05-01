import requests

messages = []
role_str = input("What role do you want to give the ai? ")
messages.append({"role": "system", "content": role_str})

while True:
    user_input = input("Enter your request: ")
    messages.append({"role": "user", "content": user_input})

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3",
            #"model": "my-rude-model", ## to install: ollama create my-rude-model -f Modelfile
            "messages": messages,
            "stream": False
        }
    )

    data = response.json()
    print(data)
    reply = response["message"]["content"]
    messages.append({"role": "assistant", "content": reply})

    print(f"Ollama says: {reply}")
    print(f"Tokens used so far: {data['prompt_eval_count']}")