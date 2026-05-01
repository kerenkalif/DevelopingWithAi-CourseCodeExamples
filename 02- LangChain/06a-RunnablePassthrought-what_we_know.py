from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

prompt = ChatPromptTemplate.from_template(
    "Tell me 3 facts about {topic}"
)

parser = StrOutputParser()

chain = prompt | llm | parser


result = chain.invoke({"topic": "dogs"})
print(result)

# 1. Dogs are loyal companions...
# 2. They can learn 200+ words...
# 3. Dogs dream like humans do
