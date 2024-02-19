# Edu Assistant
Your private, self-hosted, LLM powered learning assistant.


## Table of contents
* [General info](#general-info)
* [How to use it?](#how-to-use-it)
* [Setup](#setup)
* [Linting and formatting](#linting-and-formatting)


## General info
This project focuses on assisting in the learning process. Based on the cognitive and neuropsychological research, a set of useful tools have been established. This contains of:
* Chapters divider
* Flashcards generator
* Q&A
* *Learning session planer - WIP*

Those tools are to help by guiding and speeding up the process of reviewing the materials. If you want to get to know more about the research behind those tools and how to use them visit the section [How to use it](#how-to-use-it).

This project uses instruction tuned LLMs to process study materials such as books or research papers. This project by default uses OpenAI models, but since it uses LangChain framework, the model can be easily changed up to one's need.

Also Chroma persistent vectore store is being used to store locally the embeddings, so that the process of accessing data is much quicker each time.


## Setup
### Prerequisites
Crucial dependencies for this project (all can be found in `requirements.txt`):
* `streamlit` (1.31.0)
* `chromadb` (0.4.22)
* `langchain` (0.1.5)
* `langchain-community` (0.0.17)
* `langchain-core` (0.1.18)
* `langchain-openai` (0.0.5)

Firstly install the required dependencies by running:
```sh
pip install -r requirements.txt
```
**DISCLAIMER:** In order for the ChromaDB to work you need to have SQLite in version >3.35
SQLite is a part of Python Standard Library, so you can just update your Python to version at least 3.10 or manually update Python's DLLs, for further instructions see: [ChromaDB Troubleshooting](https://docs.trychroma.com/troubleshooting)
### Env variables
Secondly, after you have installed the required dependencies you should update your environmental variables. By default this project loades needed env variables from the `.env` file. This can be changed in the `\config.py` file.

There are 3 crucial variables that need to be set:
1. `OPENAI_API_KEY` - your OpenAI API key (If you don't want to use OpenAI models and use an open-source one instead, you must change that in code, easier method of changing a model for a whole project will be added *WIP*)
2. `PDF_FOLDER_PATH` - this is the path of where your materials in PDF format should be stored, from this path the files will be fetched for later processing
3. `PERSIST_DIRECTORY` - this is the path where the ChromaDB will be persisted for later use. If no path is set, ChromaDB will by default create its own fodler in path `chroma`

An example `.env` file might look like:
```txt
OPENAI_API_KEY=sk-abcd...
PDF_FOLDER_PATH=\\data\\
PERSIST_DIRECTORY=\\test_chromadb\\
```
### Materials
Materials must be in the PDF format and stored in the `PDF_FOLDER_PATH`. When the app is launched for the first time and there is no vectoredb stored yet, app will fetch data from all the PDF from the given directory, split the text into chunks, vectorize those chunks and persist them in the directory given in `PERSIST_DIRECTORY`.

If you want to change the matierials stored in the ChromaDB, delete the contents in `PERSIST_DIRECTORY`.
### Launch
To launch the app you simply run:
```sh
python -m streamlit run main.py
```
The browser tab should open automatically, **happy learning**!


## Linting and formatting
No linter nor formatter is being currently used: *WIP*


## How to use it
If you have already set up the project, the streamlit server is up and running and you want to get straight to learning
