from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

def create_agent_chain():
  model_name = "gpt-3.5-turbo"
  llm = ChatOpenAI(model_name=model_name)
  chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
  return chain
