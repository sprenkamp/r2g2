import os
from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory 
from langchain.vectorstores import MongoDBAtlasVectorSearch

from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()

ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]
    
#MongoDB part start

client = MongoClient(
    "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(
        ATLAS_USER, ATLAS_TOKEN))

db = client["scrape"]

#time and location from vue GUI is used here to lower the number of embeddings used (waiting for DB cahnges)
col = db["telegram"]

#MongoDB part end

api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    print('OpenAI API key not found in environment variables.')
    exit()

embeddings = OpenAIEmbeddings(openai_api_key=api_key)
vectors = MongoDBAtlasVectorSearch(
    collection=col, text_key='messageText',
    embedding=embeddings, index_name='telegram_embedding'
)

memory = ConversationBufferMemory( 
memory_key='chat_history', 
return_messages=True, 
output_key='answer')

llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=api_key)


prompt_template = """Use the following pieces of context to answer the question at the end. 
Combine the information from the context with your own general knowledge to provide a comprehensive and accurate answer. 
Please be as specific as possible, also you are a friendly chatbot who is always polite.
{context}
Question: {question}"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

chain = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=vectors.as_retriever(search_type = 'mmr', search_kwargs={'k': 100, 'lambda_mult': 0.25}), 
    memory = memory,
    return_source_documents=True,
    return_generated_question=True,
    combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
)
chat_history = []

chat_history = [chat_history]
query = input("Enter Your Query:")
answer = chain({"question": query, "chat_history": chat_history})
print(answer["source_documents"][0])
chat_history.append((query, answer["answer"]))
print(answer["answer"])