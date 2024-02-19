import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.queries import create_qa_chain, create_compression_retriever, get_precise_response, get_diversed_answer, get_compressed_context_answer

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

compression_retriever = create_compression_retriever(vectordb)
chain = create_qa_chain()

# Streamlit UI
st.set_page_config(page_title="Edu Assistant", page_icon=":book:")

with st.sidebar:
  st.header("Edu Assistant")
  st.page_link("main.py", label="Home")
  st.page_link("pages/chapters.py", label="Chapters divider")
  st.page_link("pages/flashcards.py", label="Flashcards generator")
  st.page_link("pages/qa.py", label="Q&A")

st.header("I'm here to help you with your learning!")

questions_types = [
  "Precise question",
  "Question with diversed answer",
  "Question with the compressed context"
]

type_of_question = st.radio(
  "What type of question do you want to ask?",
  questions_types
)
question = st.text_area('Enter Query')
submit = st.button("Generate")

if submit:
  with st.spinner("Loading..."):
    if type_of_question == questions_types[0]:
      st.write(get_precise_response(question, vectordb, chain))
    elif type_of_question == questions_types[1]:
      st.write(get_diversed_answer(question, vectordb, chain))
    elif type_of_question == questions_types[2]:
      st.write(get_compressed_context_answer(question, compression_retriever, chain))