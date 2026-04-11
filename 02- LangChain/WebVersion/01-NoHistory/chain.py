from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from secret_key import anthropic_key

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

template = ChatPromptTemplate.from_messages([
    ("system", "{role}"),
    ("human", "{question}")
])

chain = template | llm | StrOutputParser()


def ask_assistant2(role: str, question: str) -> str:
    return chain.invoke({"role": role, "question": question})

def ask_assistant(role: str, question: str) -> str:
    return chain.invoke({"role": f"{role}. You are not allowed to answer anything that is not relatedto your role.", 
                         "question": question})
