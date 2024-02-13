import streamlit as st

# Streamlit UI
st.set_page_config(page_title="Edu Assistant", page_icon=":book:")
st.header("I'm here to help you with your learning!")
st.subheader("Here is gonna be some project description, user onboarding/intro tutorial and research on cognitive approach to learning")

with st.sidebar:
  st.header("Edu Assistant")
  st.page_link("main.py", label="Home")
  st.page_link("pages/chapters.py", label="Chapters divider")
  st.page_link("pages/flashcards.py", label="Flashcards generator")
  st.page_link("pages/qa.py", label="Q&A")