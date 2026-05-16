from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

# --- Pydantic models ---
class JobPosition(BaseModel):
    company: str = Field(description="Company name")
    role: str = Field(description="Job title")
    reason: str = Field(description="Why it fits the candidate")

class JobSearchResult(BaseModel):
    jobs: List[JobPosition] = Field(description="List of relevant job positions")

# --- Setup ---
search = DuckDuckGoSearchRun()
llm = ChatAnthropic(model="claude-sonnet-4-6")
parser = PydanticOutputParser(pydantic_object=JobSearchResult)

prompt = ChatPromptTemplate.from_template("""
You are a job search assistant.
Based on these search results:
{search_results}

The candidate profile:
{profile}

List 3 relevant job positions.
{format_instructions}
""")

chain = (
    RunnablePassthrough.assign(
        search_results=RunnableLambda(
                lambda x: search.run(
                    f'site:drushim.co.il OR site:alljobs.co.il {x["profile"]}'
                )
            ),
        format_instructions=RunnableLambda(lambda _: parser.get_format_instructions())
    )
    | prompt
    | llm
    | parser
)

result = chain.invoke({"profile": "Python developer, 3 years experience, FastAPI, LangChain"})

for job in result.jobs:
    print(f"Company: {job.company}")
    print(f"Role:    {job.role}")
    print(f"Reason:  {job.reason}")
    print("---")