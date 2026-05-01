from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser 
from langchain_openai  import ChatOpenAI

model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
prompt_template_code = ChatPromptTemplate.from_messages(
    [
        ("system", 
 "You are a very experienced {language} developer. "
 "Write clean, well-formatted, readable Python code with proper indentation and line breaks. "
 "Do NOT use one-line compressed syntax. "
 "Return ONLY valid Python code, without markdown fences and without explanations."
),

        ("human", "write code for {app_goal}, return only the code without extra explaination text")
    ]
    )

prompt_template_unit_test = PromptTemplate(
        input_variables=["code", "langugae"],
        template="write proper unit test for the following {language} code: {code}, return only the tests code without any extra text"
)

chain_code = prompt_template_code | model | StrOutputParser()
chain_tests = prompt_template_unit_test | model | StrOutputParser()

full_chain = chain_code | {
    "code": chain_code,
    "tests": chain_tests
}   

result = full_chain.invoke({"app_goal": "sorting an array of numbers with bubble sort. the version that students learn in CS1", "language": "python"})
print("** Generated Code **")
print(result["code"])
print("** Generated Tests **")
print(result["tests"])