import streamlit as st
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")

question = st.text_input("שאל שאלה:")
if st.button("שלח"):
    response = llm.invoke(question)
    st.write(response.content)