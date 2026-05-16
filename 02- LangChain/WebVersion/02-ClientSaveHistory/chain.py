from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

parser = StrOutputParser()

def ask_assistant(role: str, question: str, history: list[dict]) -> str:
    messages = [SystemMessage(content=f"{role}. You are not allowed to answer anything that is not relatedto your role.")]

    for turn in history:
        messages.append(HumanMessage(content=turn["question"]))
        messages.append(AIMessage(content=turn["answer"]))

    messages.append(HumanMessage(content=question))

    chain = llm | parser
    return chain.invoke(messages)
