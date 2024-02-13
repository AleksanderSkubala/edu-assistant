import streamlit as st

from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db
from utils.queries import create_qa_chain, create_compression_retriever, get_compressed_context_answer

from langchain.chains import create_extraction_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)

chain = create_qa_chain()

compression_retriever = create_compression_retriever(vectordb)

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
    question = f"Give me everything a student should remember from topic: {topic}"
    terms = get_compressed_context_answer(question, compression_retriever, chain)
    print(terms)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # prompt_template_scheme = """
    # Use the following pieces of information, terms, names, etc. to create flashcards. \
    # Each flashcard must have a question and a proper answer. \
    # Flashcards must be formatted as a Python array of JSONs, each flashcard is another object with two keys: question and answer

    # Here arre the terms:
    # ###
    # {terms}
    # ###

    # Flashcards:
    # """

    # prompt_template = ChatPromptTemplate.from_template(prompt_template_scheme)
    # extraction_chain = prompt_template | llm
    # flashcards = extraction_chain.invoke({
    #   "terms": terms
    # })

    schema = {
      "properties": {
        "question": {"type": "string"},
        "answer": {"type": "string"},
      },
      "required": ["question", "answer"]
    }
    extraction_chain = create_extraction_chain(schema, llm)
    flashcards = extraction_chain.run(terms)

    with st.container(height=300):
      # st.markdown(flashcards.content)
      st.write(flashcards)