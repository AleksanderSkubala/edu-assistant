from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma

from langchain.chains import create_extraction_chain
from langchain.chains.llm import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.docstore.document import Document

from langchain.chains.prompt_selector import ConditionalPromptSelector, is_chat_model
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  SystemMessagePromptTemplate
)

from utils.queries import create_qa_chain, create_compression_retriever, get_compressed_context_answer

extraction_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
summary_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

def extract_flashcards(input_data: str) -> str:
  schema = {
    "properties": {
      "question": {"type": "string"},
      "answer": {"type": "string"},
    },
    "required": ["question", "answer"]
  }

  extraction_chain = create_extraction_chain(schema, extraction_llm)
  return extraction_chain.run(input_data)

def create_prompt_selector() -> ConditionalPromptSelector:
  # Default prompt template used when the LLM is not a chat model
  prompt_template = """
  Use the following pieces of context to create a set of flashcards on the given topic. \
  From the given pieces of context, select information that might be beneficial or important for a person studying this material to learn. \
  This information might include for example: names, terms, dates, specific words, important events, scientific phenomenons, research examples, etc. \
  Give firstly a qestion about the selected piece of information, then followed by an appropraite answer. \
  If you don't know the answer, just say that you don't know, don't try to make up an answer, use only the data and information from the given context. \

  {context}

  Topic: {question} \
  Flashcards:
  """
  prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
  )

  # Chat prompt template used when a chat model is used
  system_template = """
  You are a student creating a set of flashcards. \
  Use the following pieces of context to create a set of flashcards on the given topic. \
  From the given pieces of context, select information that might be beneficial or important for a person studying this material to learn. \
  This information might include for example: names, terms, dates, specific words, important events, scientific phenomenons, research examples, etc. \
  Give firstly a qestion about the selected piece of information, then followed by an appropraite answer. \
  If you don't know the answer, just say that you don't know, don't try to make up an answer, use only the data and information from the given context. \
  Always reffer to the given text. \

  Context: ###
  {context}
  ###
  """

  messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
  ]
  chat_prompt = ChatPromptTemplate.from_messages(messages)

  prompt_selector = ConditionalPromptSelector(
    default_prompt=prompt, conditionals=[(is_chat_model, chat_prompt)]
  )

  return prompt_selector

# A function that uses a Map and Reduce method for summaring the text, to create detailed flashcards
def create_map_reduce_chain() -> MapReduceDocumentsChain:
  map_template = """
  The following os a set of documents
  {docs}

  Use the following set of documents to create a set of flashcards on the given topic. \
  From the given set of documents, select information that might be beneficial or important for a person studying this material to learn. \
  This information might include for example: names, terms, dates, specific words, important events, scientific phenomenons, research examples, etc. \
  Give firstly a qestion about the selected piece of information, then followed by an appropraite answer. \
  If you don't know the answer, just say that you don't know, don't try to make up an answer, use only the data and information from the given context. \

  Flashcards:
  """
  map_prompt = PromptTemplate.from_template(map_template)
  map_chain = LLMChain(llm=summary_llm, prompt=map_prompt)

  reduce_template = """
  The following is set of flashcards:
  {docs}

  Take all these flashcards and combine them into a final set. \
  Your job is to do it by reducing the repeating questions, question that are very similar to each other or the questions that cover very similiar topics. \
  Try to leave as many flashcards as possible. \

  Final Flashcards:
  """
  reduce_prompt = PromptTemplate.from_template(reduce_template)
  reduce_chain = LLMChain(llm=summary_llm, prompt=reduce_prompt)

  # this will take all the summarised flashcard sets and combine into one and  pass it to the reduce chain
  combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_chain,
    document_variable_name="docs"
  )

  # combines and iteratively reduces the mapped documents
  reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
    collapse_documents_chain=combine_documents_chain,
    token_max=4000,
  )

  map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=False
  )

  return map_reduce_chain

def create_flashcards_on_topic(vectordb: Chroma, topic: str) -> str:
  prompt_selector = create_prompt_selector()
  chain = create_qa_chain(prompt_selector)
  compression_retriever = create_compression_retriever(vectordb)

  question = f"The topic is: {topic}"

  terms = get_compressed_context_answer(question, compression_retriever, chain)
  print(terms)
  return extract_flashcards(terms)

def create_flashcards_generally(docs: list[Document]) -> str:
  chain = create_map_reduce_chain()
  terms = chain.run(docs)
  return terms