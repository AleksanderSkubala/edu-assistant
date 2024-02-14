from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

from langchain.chains import create_extraction_chain

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

def extract_data(input_data, schema):
  extraction_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
  extraction_chain = create_extraction_chain(schema, extraction_llm)
  return extraction_chain.run(input_data)

def summarize_docs(docs, type, schema):
  chain = load_summarize_chain(llm, chain_type=type)
  summary = chain.run(docs)

  return extract_data(summary, schema)

def get_general_topics(docs):
  schema = {
    "properties": {
      "general_topics": {
        "type": "array",
        "items": {"type": "string"}
      },
    },
    "required": ["general_topics"]
  }

  return summarize_docs(docs, "stuff", schema)

def get_detailed_topics(docs):
  schema = {
    "properties": {
      "topics": {
        "type": "array",
        "items": {"type": "string"}
      },
    },
    "required": ["topics"]
  }

  return summarize_docs(docs, "map_reduce", schema)

def get_combined_topics(docs):
  schema = {
    "properties": {
      "general_topics": {
        "type": "array",
        "items": {"type": "string"}
      },
      "detailed_topics": {
        "type": "array",
        "items": {"type": "string"}
      },
    },
    "required": ["general_topics", "detailed_topics"]
  }

  return summarize_docs(docs, "stuff", schema)