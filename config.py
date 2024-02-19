import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
pdf_folder_path = os.environ.get("PDF_FOLDER_PATH", "/data")
persist_directory = os.environ.get("PERSIST_DIRECTORY")
