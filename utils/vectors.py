import os

from config import api_key

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter

# from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

def fetch_and_chunk_documents(pdf_folder_path: str) -> list:
  documents = []
  for file in os.listdir(pdf_folder_path):
    if file.endswith('.pdf'):
      file_path = os.path.join(pdf_folder_path, file)
      print(f"Processing files: {file_path}")
      doc_loader = PyPDFLoader(file_path, extract_images=True)
      documents.extend(doc_loader.load())
      print(f"File {file_path} is done")
  print(f"Splitting text...")
  text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
  chunked_documents = text_splitter.split_documents(documents)
  print(f"The text is splitted")
  return chunked_documents

def load_vector_db(pdf_folder_path: str, persist_directory: str) -> Chroma:
  print(f"Vectordb is being created in {persist_directory}")
  embedding_function = OpenAIEmbeddings()
  persistent_client = chromadb.PersistentClient(path=persist_directory)

  if persistent_client.list_collections():
    print("VectorDB is already created")
    langchain_chroma = Chroma(
      client=persistent_client,
      collection_name="docs_collection",
      embedding_function=embedding_function
    )
    return langchain_chroma
  else:
    docs = fetch_and_chunk_documents(pdf_folder_path)

    langchain_chroma = Chroma.from_documents(
      docs,
      client=persistent_client,
      collection_name="docs_collection",
      embedding=embedding_function
    )

    print("VectorDB has been persisted")

    return langchain_chroma




