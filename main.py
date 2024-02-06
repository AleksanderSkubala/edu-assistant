import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.queries import create_qa_chain, create_compression_retriever, get_precise_response, get_diversed_answer, get_compressed_context_answer

# model_name = "gpt-3.5-turbo"
model_name = "gpt-4"

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

compression_retriever = create_compression_retriever(vectordb, model_name)
chain = create_qa_chain(model_name)

# Streamlit UI
st.set_page_config(page_title="Edu Assistant", page_icon=":book:")
st.header("I'm here to help you with your learning!")

types_of_questions = [
  "Precise question",
  "Question with diversed answer",
  "Question for the whole context"
]

type_of_question = st.radio(
  "What type of question do you want to ask?",
  types_of_questions
)
question = st.text_input('Enter Query')
submit = st.button("Generate")

if submit:
  if type_of_question == type_of_question[0]:
    st.write(get_precise_response(question, vectordb, chain))
  elif type_of_question == type_of_question[1]:
    st.write(get_diversed_answer(question, vectordb, chain))
  elif type_of_question == type_of_question[2]:
    st.write(get_compressed_context_answer(question, compression_retriever, chain))