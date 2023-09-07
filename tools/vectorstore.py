# vector store pinecone
import os

import pinecone
from langchain.chains import question_answering
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import Pinecone

with open("openai_api_key.txt", "r") as f:
    api_key = f.read()
    
with open("pinecone_api.txt", "r") as f:
    pinecone_api_key = f.read()
    
    
os.environ["OPENAI_API_KEY"] = api_key

llm = OpenAI(
    temperature=0.4,
)


def initialize_vectordb():
    """Initialize the vector database"""
    vectors = pinecone.init(
        api_key=pinecone_api_key,
        environment="northamerica-northeast1-gcp"
    )
    return vectors


def vectordb(query: str):
    vector = initialize_vectordb()
    search = Pinecone.from_existing_index(
        index_name="index-1",
        embedding=OpenAIEmbeddings(),
        namespace="clinic"
    )
    similar_docs = search.as_retriever(search_type="mmr").get_relevant_documents(query=query)
    # write a Q and A chain to get the answer
    qachain = question_answering.load_qa_chain(
        llm=llm,
        chain_type="stuff",
        
    )
    return qachain.run(input_documents=similar_docs, question=query)
