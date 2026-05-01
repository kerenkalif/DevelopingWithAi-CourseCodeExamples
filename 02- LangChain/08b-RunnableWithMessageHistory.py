from config import anthropic_model
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatAnthropic(model=anthropic_model)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a useful assistant."),
    MessagesPlaceholder(variable_name="history"),  # ← כאן תוכנס ההיסטוריה
    ("human", "{input}"),
])

chain = prompt | llm

# a dictionary: session_id → ChatMessageHistory
store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "user_1"}}

response = chain_with_history.invoke(
    {"input": "My name is Keren. What is your name?"},
    config=config
)
print(response.content)

response = chain_with_history.invoke(
    {"input": "What is my name?"},
    config=config
)
print(response.content) # should be 'Keren'
