import streamlit as st

user_input = st.text_input("מה שמך?")
st.write(f"שלום, {user_input}!")