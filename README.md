# Edu Assistant
Your private, self-hosted, LLM powered learning assistant.


## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Linting and formatting](#linting-and-formatting)
* [How to use it?](#how-to-use-it)
* [Research](#research)


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
If you have already set up the project, the streamlit server is up and running and you want to get straight to learning, here is the short brief on learning methods assisted by this app and how to use them.

This app bases on two crucial research-based methods of learning enhancing:
1. **Spaced repetition** - spreading learning over time
2. **Active recall** - using methods of self-questioning to improve the creation of the memory track/footprint

You may read about the scientific specifics of those below, right now we're going to focus on how to help ourselves with Edu Assitant.
### Spaced repetition
Your brain remembers the best when you give him time to partly forget the information you try to acquire. Firstly, go into the `Chapter divider` section of the Edu Assistent. Here you can get the main motives/chapters/topics of your materials.
* `General topics` are the main chapters that appear in the text, but those might be to big to learn in one sitting.
* `Detailed topics` are the more precise ones, usually also the smaller ones.

When you have the topics generated now it's time to plan learning sessions. The section with an automated planner is still in progress so now you can do it by hand. Here are methods on how to plan your learning sessions:
1. **Wozniak's time intervals**
2. **Leitner's system**
3. **Benedict Carey's optimal intervals**

*(to be described in detail in next iteravtions)*
### Active recall
When you have your sessions planned and you now what topics to cover it's time to start learning! There are many methods of practicing active recall, those might involve specific note taking methods, self-generating quizzes and flashcards. We are going to focus on the latter.

Generating flashcards can be really time consuming, and yes, preparing flashcards on your own is beneficial to the learning process, but we all know when the end of the term is coming we do not have the luxury of having time.  Edu Assistant is here to help, go into the section `Flashcards generator` and pick one of the two options:
1. `a specific topic` - You can specify the subtopic you want to get the flashcards about. Please don't be to specific, this way you will get only a couple of flashcards if at all more than one. The flashcards are exported in a JSON format so it is easier to import it in apps like Anki, SuperMemo or OmniSets.
2. `the whole document` - Altough it takes a minute or two, it generates a flashcards set out of the whole document. Extraction of this many flashcards to JSON does not work yet (*WIP*).

When you are studying your flashcards accordingly to your study plan, and you come across a question that you would like to know more about, you can simply ask your assistant. In the section `Q&A` you may ask any question abouyt given materials.

1. `Specific question` searches for the most relevant chunk of material and passes it as a context along with a question you want ask the LLM
2. `Question with a diverse answer` works simply the same as the precise question but looking for the relevant chunks takes into consideration the most diverse but still relevant parts (see Maximal Marginal Relevance search)
3. `Question with the compressed context` compresses all the relevant chunks of information and passes the compressed summary as a context

With those three you can ask about basically anything, you can also give instructions like: "explain" or "give an analogy", just like it were your teacher.

## Research (to be finished)
### Spaced repetition
### Active recall
84% of college students rely on rereading as a study strategy, although it is considered to be the **least effective** method of all.

The base of any learning system is active recall which involves testing, information retrieval and comprehension. Usually it means flashcards or self-generated questions, tests or quizzes. Active recall is also reffered to as "practive testing" or "retrieval practice". Active recall can be self-directed but also practiced with others.
### Further reading
[Smolen P, Zhang Y, Byrne JH. The right time to learn: mechanisms and optimization of spaced learning. Nat Rev Neurosci. 2016](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5126970/)

[Moulton CA, Dubrowski A, Macrae H, Graham B, Grober E, Reznick R. Teaching surgical skills: what kind of practice makes perfect?: a randomized, controlled trial. Ann Surg. 2006](https://pubmed.ncbi.nlm.nih.gov/16926566/)

[Pyc MA, Rawson KA. Examining the efficiency of schedules of distributed retrieval practice. Mem Cognit. 2007](https://pubmed.ncbi.nlm.nih.gov/18265608/)

[How to Remember More of What You Learn with Spaced Repetition](https://collegeinfogeek.com/spaced-repetition-memory-technique/)

[Spaced Repetition: A Guide to the Technique](https://e-student.org/spaced-repetition/)

[Active Recall: What It Is, How It Works, and More](https://e-student.org/active-recall-study-method/)