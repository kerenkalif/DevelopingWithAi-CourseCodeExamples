from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import anthropic_model

llm = ChatAnthropic(model=anthropic_model)
parser = StrOutputParser()

store = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def build_chain(role: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"{role}. You are not allowed to answer anything not related to your role."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    chain = prompt | llm | parser
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

def ask_assistant(role: str, question: str, session_id: str) -> str:
    chain = build_chain(role)
    return chain.invoke(
        {"input": question},
        config={"configurable": {"session_id": session_id}}
    )