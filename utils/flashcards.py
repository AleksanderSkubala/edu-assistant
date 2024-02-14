from langchain.chains import create_extraction_chain
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate

question = f"""
Give me everything a student should remember from topic: {topic} \
This includes: names, terms, dates, specific words, important events, scientific phenomenons, research examples, etc. \
Include everything that could be possibly important for a person studying this materials
"""
terms = get_compressed_context_answer(question, compression_retriever, chain)
print(terms)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

schema = {
  "properties": {
    "question": {"type": "string"},
    "answer": {"type": "string"},
  },
  "required": ["question", "answer"]
}
extraction_chain = create_extraction_chain(schema, llm)
flashcards = extraction_chain.run(terms)
