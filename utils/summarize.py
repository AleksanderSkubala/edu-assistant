from langchain_openai import ChatOpenAI
from langchain.chains import load_summarize_chain
from langchain.docstore.document import Document
from langchain.chains import create_extraction_chain

from typing import Literal

type SummaryChainType = Literal["stuff", "map_reduce", "refine"]

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106")

def extract_data(input_data: str, schema: object) -> str:
  extraction_llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
  extraction_chain = create_extraction_chain(schema, extraction_llm)
  return extraction_chain.run(input_data)

def summarize_docs(docs: list[Document], type: SummaryChainType, schema: object) -> str:
  chain = load_summarize_chain(llm, chain_type=type)
  summary = chain.run(docs)

  return extract_data(summary, schema)

def get_general_topics(docs: list[Document]) -> str:
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

def get_detailed_topics(docs: list[Document]) -> str:
  schema = {
    "properties": {
      "detailed_topics": {
        "type": "array",
        "items": {"type": "string"}
      },
    },
    "required": ["topics"]
  }

  return summarize_docs(docs, "map_reduce", schema)

def get_combined_topics(docs: list[Document]) -> str:
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