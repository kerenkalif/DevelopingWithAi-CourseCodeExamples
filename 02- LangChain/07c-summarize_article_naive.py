import tkinter as tk
from tkinter import filedialog
from pypdf import PdfReader

from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import time

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

the_article = get_file_content()

time1 = time.perf_counter()
summary = summary_chain.invoke({"article": the_article})
time2 = time.perf_counter()
print(f"### FINISHED SUMMARY ({time2-time1} ms)")

terms = terms_chain.invoke({"article": the_article})
time3 = time.perf_counter()
print(f"### FINISHED TERMS ({time3-time2} ms)")

level = level_chain.invoke({"article": the_article})
time4 = time.perf_counter()
print(f"### FINISHED LEVEL ({time4-time3} ms)")

result = {
    "summary": summary,
    "terms":   terms,
    "level":   level,
}

print(f"### SUMMARY:\n {result['summary']}")
print(f"### TERMS:\n {result['terms']}")
print(f"### LEVEL:\n {result['level']}")


