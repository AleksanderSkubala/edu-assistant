import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.summarize import default_summarize_chain, stuff_summarize

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

st.set_page_config(page_title="Edu Assistant", page_icon=":book:")
st.header("I'm here to help you with your learning!")

with st.sidebar:
  st.header("Edu Assistant")
  st.page_link("main.py", label="Home")
  st.page_link("pages/chapters.py", label="Chapters divider")
  st.page_link("pages/flashcards.py", label="Flashcards generator")
  st.page_link("pages/qa.py", label="Q&A")

submit = st.button("Generate summary")

if submit:
  with st.spinner("Loading..."):
    with st.container(height=300):
      print(vectordb.get()["documents"])
      summary = default_summarize_chain(vectordb.similarity_search(" "))
      st.markdown(summary)