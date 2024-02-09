from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

from langchain.chains.prompt_selector import ConditionalPromptSelector, is_chat_model
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
  ChatPromptTemplate,
  HumanMessagePromptTemplate,
  SystemMessagePromptTemplate
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def create_prompt_selector():
  # Default prompt template used when the LLM is not a chat model
  prompt_template = """
  Use the following pieces of context to answer the question at the end. \
  If you don't know the answer, just say that you don't know, don't try to make up an answer. \

  {context}

  Question: {question} \
  Answer:
  """
  prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
  )

  # Chart prompt template used when a chat model is used
  system_template = """
  You are a student taking an open book test. Use the pieces of context to answer the question. \
  Always reffer to the given text. \
  If you don't know the answer, don't try to make it up, say that you don't know. \
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


def create_qa_chain():
  prompt_selector = create_prompt_selector()
  chain = load_qa_chain(
    llm,
    chain_type="stuff",
    verbose=True,
    prompt=prompt_selector.get_prompt(llm)
  )
  return chain

def create_compression_retriever(vectordb):
  compressor = LLMChainExtractor.from_llm(llm)

  compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectordb.as_retriever()
  )

  return compression_retriever

def get_precise_response(query: str, vectordb, chain):
  matching_chunks = vectordb.similarity_search(query,k=3)
  print("Chunks of text matching the question:")

  print("Chunks of text matching the question:")
  for chunk in matching_chunks:
    print(f"Page number: {chunk.metadata["page"]}")

  answer = chain.run(input_documents=matching_chunks, question=query)
  return answer

def get_diversed_answer(query, vectordb, chain):
  # based on Maximum Marginal Relevance (MMR)
  matching_chunks = vectordb.max_marginal_relevance_search(query,k=2, fetch_k=2)

  print("Chunks of text matching the question:")
  for chunk in matching_chunks:
    print(f"Page number: {chunk.metadata["page"]}")

  answer = chain.run(input_documents=matching_chunks, question=query)
  return answer

def get_compressed_context_answer(query, compression_retriever, chain):
  # based on Context Compression
  matching_chunks = compression_retriever.get_relevant_documents(query)
  print("Chunks of text matching the question:")

  print("Chunks of text matching the question:")
  for chunk in matching_chunks:
    print(f"Page number: {chunk.metadata["page"]}")


  answer = chain.run(input_documents=matching_chunks, question=query)
  return answer