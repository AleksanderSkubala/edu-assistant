from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain

from langchain.prompts import PromptTemplate
from langchain.chains import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

def default_summarize_chain(docs):
  chain = load_summarize_chain(llm, chain_type="stuff")
  result = chain.run(input_documents=docs, question="Write in points main chapters that occured in this passage")
  return result

def map_and_reduce_summary(docs):
  # Define prompt
  prompt_template = """Write in points main chapters that occured in this passage:
  "{text}"
  CONCISE SUMMARY:"""
  prompt = PromptTemplate.from_template(prompt_template)

  # Define LLM chain
  # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
  llm_chain = LLMChain(llm=llm, prompt=prompt)

  # Define StuffDocumentsChain
  stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

  # docs = loader.load()
  result = stuff_chain.run(docs)
  return result