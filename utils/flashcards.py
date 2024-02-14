from langchain_openai import ChatOpenAI

from langchain.chains.question_answering import load_qa_chain
from langchain.chains import create_extraction_chain

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

def extract_flashcards(input_data):
  schema = {
    "properties": {
      "question": {"type": "string"},
      "answer": {"type": "string"},
    },
    "required": ["question", "answer"]
  }

  extraction_chain = create_extraction_chain(schema, extraction_llm)
  return extraction_chain.run(input_data)

def create_prompt_selector():
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



def create_flashcards_on_topic(vectordb, topic):
  prompt_selector = create_prompt_selector()
  chain = create_qa_chain(prompt_selector)
  compression_retriever = create_compression_retriever(vectordb)

  question = f"The topic is: {topic}"

  terms = get_compressed_context_answer(question, compression_retriever, chain)
  return extract_flashcards(terms)

def create_flashcards_generally(docs):
  return docs