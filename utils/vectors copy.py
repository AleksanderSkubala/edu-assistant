import os

from config import api_key

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from langchain_community.vectorstores import Chroma
import chromadb

def fetch_and_chunk_documents(pdf_folder_path: str) -> list:
  documents = []
  for file in os.listdir(pdf_folder_path):
    if file.endswith('.pdf'):
      file_path = os.path.join(pdf_folder_path, file)
      print(f"Processing files: {file_path}")
      # pip install rapidocr-onnxruntime for exctracting images
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

  # embeddings = OpenAIEmbeddings(
  #   model_name="text-embedding-ada-002"
  # )
  embeddings = OpenAIEmbeddings()
  persistent_client = chromadb.PersistentClient(path=persist_directory)

  if persistent_client.list_collections():
    print("VectorDB is already created")
    return persistent_client.get_collection("docs_collection", embedding_function=embeddings)
  else:
    docs = fetch_and_chunk_documents(pdf_folder_path)

    Chroma.from_documents(
      docs,
      embeddings,
      client=persistent_client,
      collection_name="docs_collection",
      collection_metadata={"hnsw:space": "cosine"}
    )
    print("VectorDB has been persisted")

    return persistent_client.get_collection("docs_collection", embedding_function=embeddings)




