from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

prompt = ChatPromptTemplate.from_template(
    "Tell me 3 facts about {topic}"
)
parser = StrOutputParser()
chain = prompt | llm | parser

topic = "dogs"
facts = chain.invoke({"topic": topic})
topic_as_title = topic.upper()

result = {
    "topic": topic,
    "facts": facts,
    "topic_as_title": topic_as_title,
}

print(result)

