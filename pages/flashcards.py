import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

# Streamlit UI
st.set_page_config(page_title="Edu Assistant", page_icon=":book:")

with st.sidebar:
  st.header("Edu Assistant")
  st.page_link("main.py", label="Home")
  st.page_link("pages/chapters.py", label="Chapters divider")
  st.page_link("pages/flashcards.py", label="Flashcards generator")
  st.page_link("pages/qa.py", label="Q&A")

topic = st.text_input("Provide a topic of which you want to have flashcards")
submit = st.button("Generate")

if submit:
  with st.spinner("Loading..."):


    with st.container(height=300):
      # st.markdown(flashcards.content)
      st.write(flashcards)