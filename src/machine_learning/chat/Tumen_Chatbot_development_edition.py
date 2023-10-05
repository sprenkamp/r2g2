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
import datetime

app = FastAPI()

ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]

def parse_parameters(start_date, end_date, country, state):
    must_conditions = []
    if state != 'null':
        filter = {
            "text": {
                "path": "state",
                "query": state
            }
        }
        must_conditions.append(filter)

    if country != 'null':
        filter = {
            "text": {
                "path": "country",
                "query": country
            }
        }
        must_conditions.append(filter)

    start_date = '1999-01-01' if start_date == 'null' else start_date
    end_date = '2999-01-01' if end_date == 'null' else end_date
    filter = {
        'range': {
            'path': 'messageDatetime',
            'gte': datetime.datetime.strptime(start_date, "%Y-%m-%d"),
            'lte': datetime.datetime.strptime(end_date, "%Y-%m-%d")+datetime.timedelta(days=1),
        }
    }
    must_conditions.append(filter)

    conditions = {
        "compound": {
            "must": must_conditions
        }
    }

    return conditions

@app.post("/query")
def query(start_date, end_date, country, state, query, chat_history):
    '''

    Args:
        start_date: string, e.g. '2022-01-01'
        end_date: string e.g. '2022-01-02'
        country: string e.g. 'Switzerland'
        state: string e.g. 'Zurich'
        query: string e.g. 'Can I get free clothes in Zurich?'
        chat_history: array

    Returns:

    '''
    
    # initialize
    client = MongoClient(
        "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(
            ATLAS_USER, ATLAS_TOKEN))
    db_name, collection_name = "test", "telegram"
    collection = client[db_name][collection_name]

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print('OpenAI API key not found in environment variables.')
        exit()

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vectors = MongoDBAtlasVectorSearch(
        collection=collection, text_key='messageText',
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

    # generate conditions
    must_conditions = parse_parameters(start_date, end_date, country, state)

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectors.as_retriever(search_type = 'mmr',
                                       search_kwargs={
                                                'k': 100, 'lambda_mult': 0.25,
                                                "pre_filter": {
                                                   "compound": {
                                                       "must": must_conditions
                                                   }
                                                },
                                       }),
        memory = memory,
        return_source_documents=True,
        return_generated_question=True,
        combine_docs_chain_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    chat_history = [chat_history]
    answer = chain({"question": query, "chat_history": chat_history})
    print(answer["source_documents"][0])
    return answer["answer"]
