import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.flashcards import create_flashcards_on_topic, create_flashcards_generally

from langchain.docstore.document import Document

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

st.header("I'm here to help you with your learning!")

flashcards_set_types = [
  "a specific topic",
  "the whole document",
]

type_of_flashcards_set = st.radio(
  "Generate flaschcards on:",
  flashcards_set_types
)

topic = ""
if type_of_flashcards_set == flashcards_set_types[0]:
  topic = st.text_input("Provide a topic of which you want to have flashcards")

submit = st.button("Generate")

if submit:
  with st.spinner("Loading..."):
    flashcards = []
    if type_of_flashcards_set == flashcards_set_types[0]:
      flashcards = create_flashcards_on_topic(vectordb, topic)
    if type_of_flashcards_set == flashcards_set_types[1]:
      all_texts = vectordb.get()["documents"]
      all_metadatas = vectordb.get()["metadatas"]

      docs = []
      for doc_index in range(len(all_texts)):
        page = Document(
          page_content=all_texts[doc_index],
          metadata=all_metadatas[doc_index]
        )
        docs.append(page)

      flashcards = create_flashcards_generally(docs)

    with st.container(height=300):
      st.write(flashcards)