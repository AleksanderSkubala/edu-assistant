import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.summarize import get_combined_topics, get_general_topics, get_detailed_topics

from langchain.docstore.document import Document

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

st.set_page_config(page_title="Edu Assistant", page_icon=":book:")

with st.sidebar:
  st.header("Edu Assistant")
  st.page_link("main.py", label="Home")
  st.page_link("pages/chapters.py", label="Chapters divider")
  st.page_link("pages/flashcards.py", label="Flashcards generator")
  st.page_link("pages/qa.py", label="Q&A")

st.header("I'm here to help you with your learning!")

summary_types = [
  "Only general topics",
  "Only detailed topics",
  "General and detailed topics"
]

type_of_summary = st.radio(
  "What type of summary do you want to generate?",
  summary_types
)

submit = st.button("Generate summary")

if submit:
  with st.spinner("Loading..."):
    all_texts = vectordb.get()["documents"]
    all_metadatas = vectordb.get()["metadatas"]

    docs = []
    for doc_index in range(len(all_texts)):
      page = Document(
        page_content=all_texts[doc_index],
        metadata=all_metadatas[doc_index]
      )
      docs.append(page)

    summary = {}

    if type_of_summary == summary_types[0]:
      summary = get_general_topics(docs)
    if type_of_summary == summary_types[1]:
      summary = get_detailed_topics(docs)
    if type_of_summary == summary_types[2]:
      summary = get_combined_topics(docs)

    with st.container(height=300):
      st.write(summary)