from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser

def get_pretty_web_search_results(search_answer):
    format_prompt = ChatPromptTemplate.from_template("""
    Format these search results as a numbered list, one result per line:
    {results}
    """)

    format_chain = format_prompt | llm | StrOutputParser()
    formatted = format_chain.invoke({"results": search_answer})
    return formatted

query = "Tell me about AlgoTracer."

# --- LLM only ---
llm = ChatAnthropic(model="claude-sonnet-4-6")
prompt = ChatPromptTemplate.from_template("Answer this question: {question}")
llm_chain = prompt | llm | StrOutputParser()

llm_answer = llm_chain.invoke({"question": query})

# --- Web search ---
search = DuckDuckGoSearchRun()
search_answer = search.run(query)

# --- Compare ---
print("=== LLM Answer ===")
print(llm_answer)
print("\n=== Web Search Answer ===")
print(get_pretty_web_search_results(search_answer))

