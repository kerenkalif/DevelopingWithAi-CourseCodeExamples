from google import genai
from google.genai import types

client = genai.Client()

role_str = input("What role do you want to give the ai? ")
chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=role_str
        )
    )

#messages = []
while True:
    user_input = input("Enter your request: ")
    resp = chat.send_message(user_input)
    print(f"Full response structure:\n{resp.model_dump_json(indent=2)}")

    print(f"Gemini says: {resp.text}")

    if resp.usage_metadata:
        print(f"Input tokens used so far: {resp.usage_metadata.prompt_token_count}")
        print(f"Output tokens used so far: {resp.usage_metadata.candidates_token_count}")
        print(f"Total tokens used so far: {resp.usage_metadata.total_token_count}")





