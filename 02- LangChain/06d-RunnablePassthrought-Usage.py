from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
parser = StrOutputParser()

facts_prompt = ChatPromptTemplate.from_template(
    "Tell me 3 facts about {topic}"
)

facts_chain = facts_prompt | llm | parser

enriched_facts = RunnablePassthrough.assign(
    topic_as_title=lambda x: x["topic"].upper(),
    facts=facts_chain,
)

marketing_prompt = ChatPromptTemplate.from_template(
    "Write marketing content titled '{topic_as_title}' "
    "using these facts: {facts}"
)

marketing_chain = marketing_prompt | llm | parser
full_pipeline = enriched_facts | marketing_chain
#full_pipeline = enriched_facts | marketing_prompt | llm | parser


marketing_text = full_pipeline.invoke({"topic": "dogs"})
print(marketing_text)