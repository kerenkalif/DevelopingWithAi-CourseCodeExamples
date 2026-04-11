from anthropic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from secret_key import anthropic_key

import os
os.environ["ANTHROPIC_API_KEY"] = anthropic_key

class Cake(BaseModel):
    name:        str
    diameter_cm: int
    is_dairy:    bool
    price:       float


llm = ChatAnthropic(model="claude-haiku-4-5-20251001", api_key=anthropic_key)

messages = []
messages.append(HumanMessage("Describe a chocolate cake. Return JSON with: name, diameter_cm, is_dairy, price"))

response = llm.invoke(messages)

parser = PydanticOutputParser(pydantic_object=Cake)
cake = parser.invoke(response)
print(f"{cake.diameter_cm} --> {type(cake.diameter_cm)}")   
print(f"{cake.price} --> {type(cake.price)}")  
