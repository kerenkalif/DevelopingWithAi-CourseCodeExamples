from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()

history.add_user_message("Which city is the capital of France?")
history.add_ai_message("Paris.")
history.add_user_message("And what is the size of its population?")

for message in history.messages:
    print(f"{message.type}: {message.content}")
