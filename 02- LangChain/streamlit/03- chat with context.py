import streamlit as st
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-4-6")

if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("שאל שאלה:")
if st.button("שלח") and question:
    messages = st.session_state.history + [{"role": "user", "content": question}]
    response = llm.invoke(messages)
    st.session_state.history.append({"role": "user", "content": question})
    st.session_state.history.append({"role": "assistant", "content": response.content})
    st.rerun()

for msg in st.session_state.history:
    prefix = "את/ה: " if msg["role"] == "user" else "Assistant: "
    st.write(prefix + msg["content"])