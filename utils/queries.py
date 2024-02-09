from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

def create_prompt_template():
  return "abd"

def create_qa_chain(model_name):
  llm = ChatOpenAI(model_name=model_name, temperature=0)
  chain = load_qa_chain(
    llm,
    chain_type="stuff",
    verbose=True
  )
  return chain

def create_compression_retriever(vectordb, model_name):
  llm = ChatOpenAI(model_name=model_name, temperature=0)
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