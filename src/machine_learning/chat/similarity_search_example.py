import os
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# In order to achieve similarity searching, we need:
# (1) Set up openAI key.
# (2) Generate embedding and store them in collection.
#     Note: We must apply the same embedding rules to both training text and query!
#     Check source code,
#         https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html
#     we can find MongoDB use 'self._embedding.embed_query(query)' to generate embedding for query.
#     We probably will not get similar documents if we use different embedding rules,
#         e.g, OpenAIEmbeddings for query, bert model for training
# (3) create Vector index on Atlas website (cluster->search->create index).

# My concern
# (1) Cost for training embedding using OpenAI API.
#    -> maybe we can change source code in MongoDBAtlasVectorSearch(). Enable to use open source embedding model
# (2) whether Vector Index is strong enough to find relevant docs less than x second (we have 2 million data)

# initialize database
ATLAS_TOKEN = os.environ["ATLAS_TOKEN"]
ATLAS_USER = os.environ["ATLAS_USER"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
client = MongoClient(
    "mongodb+srv://{}:{}@cluster0.fcobsyq.mongodb.net/".format(
        ATLAS_USER, ATLAS_TOKEN))

# initialize vector store
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
db_name = "test"
collection_name = "telegram_sample"  # 1 embedding using OpenAI, 45 embeddings using bert. So only one item has high similarity below
collection = client[db_name][collection_name]
vectorstore = MongoDBAtlasVectorSearch(
    collection=collection, text_key='messageText',
    embedding=embeddings, index_name='telegram_embedding'
)

# Function1: perform a similarity search between a query and the ingested documents
query = "Can I find jobs as a nurse?"
retriever = vectorstore.as_retriever()
relevant_docs = retriever.get_relevant_documents(query)
print(relevant_docs)  # only one record will be matched
print("--*--"*3, "relevant doc above", "--*--"*3)

# submit query and relevant data to OpenAI
query = "Can I find jobs as a nurse?"
history = []
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0.0, model_name='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY),
    retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={'k': 5, 'lambda_mult': 0.25})
)
ans = chain({"question": query, "chat_history": []})["answer"]
print(ans)


# ----------- something might be helpful -----------
# How to generate embedding using OpenAIEmbeddings
# text = "Vacancy WITHOUT LANGUAGE KNOWLEDGE!"
# query_result = embeddings.embed_query(text)
# print(query_result)

