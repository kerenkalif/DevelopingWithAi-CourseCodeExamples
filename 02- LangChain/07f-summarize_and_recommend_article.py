import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def get_file_content():
    # 1. Initialize tkinter and hide the main window
    root = tk.Tk()
    root.withdraw()
    
    # 2. Open the file dialog
    file_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")]
    )
    
    if not file_path:
        print("No file was selected.")
        return

    try:
        # 3. Load the PDF file
        reader = PdfReader(file_path)
        the_text = ""
        for i, page in enumerate(reader.pages):
                the_text += page.extract_text()
        return the_text
            
    except Exception as e:
        print(f"An error occurred: {e}")


llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
parser = StrOutputParser()

summary_prompt = ChatPromptTemplate.from_template("Summarize in max 300 words this article: {article}")
terms_prompt = ChatPromptTemplate.from_template("List terms of this article: {article}")
level_prompt = ChatPromptTemplate.from_template("Rate difficulty of this article: {article}")

summary_chain = summary_prompt | llm | parser
terms_chain   = terms_prompt   | llm | parser
level_chain   = level_prompt   | llm | parser

analysis = {
    "summary": summary_chain,
    "terms": terms_chain,
    "level": level_chain,
}

report_prompt = ChatPromptTemplate.from_template("""
Based on the analysis below,
write a short learning recommendation:
- Who should read this article?
- What is the estimated reading time?
- What prerequisites are needed?

Summary: {summary}
Key terms: {terms}
Difficulty: {level}
""")

report_chain = report_prompt | llm | parser
full_pipeline = analysis | report_chain

print("START")
the_article = get_file_content()
recommendation = full_pipeline.invoke(
    {"article": the_article})

print(f"###Recommendation:\n{recommendation}")

