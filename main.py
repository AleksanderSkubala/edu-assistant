import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.queries import create_agent_chain

def get_response(query: str):
  matching_chunks = vectordb.similarity_search(query,k=3)
  print("Chunks of text matching the question:")
  print(f"{matching_chunks}")

  answer = chain.run(input_documents=matching_chunks, question=query)
  return answer

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)
chain = create_agent_chain()

# print(get_response("What are the two principles on genetics and behaviour?"))


# Streamlit UI
st.set_page_config(page_title="Edu Assistant", page_icon=":book:")
st.header("Ask me anything about Psychology (from the PDF)")

form_input = st.text_input('Enter Query')
submit = st.button("Generate")

if submit:
    st.write(get_response(form_input))