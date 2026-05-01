from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
parser = StrOutputParser()

facts_prompt = ChatPromptTemplate.from_template(
    "Tell me 3 facts about {topic}"
)

facts_chain = facts_prompt | llm | parser

topic = "dogs"
facts = facts_chain.invoke({"topic": topic})

print("### facts text:\n" + facts)

result = {
    "topic": topic,
    "facts": facts,
    "topic_as_title": topic.upper(),
}

marketing_prompt = ChatPromptTemplate.from_template(
    "Write marketing content titled '{topic_as_title}' "
    "using these facts: {facts}"
)
marketing_chain = marketing_prompt | llm | parser

marketing_text = marketing_chain.invoke(result)
print("### marketing text:\n" + marketing_text)