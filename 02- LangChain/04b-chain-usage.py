from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Cake(BaseModel):
    name:        str
    diameter_cm: int
    is_dairy:    bool
    price:       float

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
parser = PydanticOutputParser(pydantic_object=Cake)

chain = llm | parser

cake = chain.invoke([HumanMessage(
    "Describe a chocolate cake. "
    "Return JSON with: name, diameter_cm, is_dairy, price"
)])
print(cake.name)
print(cake.price)