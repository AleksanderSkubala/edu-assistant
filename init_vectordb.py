from config import pdf_folder_path, persist_directory
from utils.vectors import load_vector_db

vectordb = load_vector_db(
  pdf_folder_path,
  persist_directory
)