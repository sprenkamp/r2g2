import sys
sys.path.append("src/langchain_agent/")

from chroma_retrieve import retrieve_chromadb
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

vectordb = retrieve_chromadb(collection_name="one_piece")

def chat(message: str) -> str:
    # Build prompt
    prompt_template = """Use the following pieces of context to answer the question at the end. Combine the information from the context with your own general knowledge to provide a comprehensive and accurate answer. Please be as specific as possible, and don't include information that is not corroborated by the context or your general knowledge.
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'lambda_mult': 0.25}), # Retrieve more documents with higher diversity- useful if your dataset has many similar documents
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    result = qa_chain({"query": message})
    print(result)

    return result["result"]
