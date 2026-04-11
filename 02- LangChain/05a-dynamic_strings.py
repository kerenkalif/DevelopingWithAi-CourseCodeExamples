from langchain_core.messages import SystemMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from secret_key import anthropic_key

class Cake(BaseModel):
    name:        str
    diameter_cm: int
    is_dairy:    bool
    price:       float

llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

domain = "pastry"
topic  = "chocolate cake"

parser = PydanticOutputParser(pydantic_object=Cake)

response = llm.invoke([
    SystemMessage(f"You are an expert in {domain}"),
    HumanMessage(f"Describe a {topic}. Return JSON with: name, diameter_cm, is_dairy, price")
])
cake = parser.invoke(response)
print(cake)