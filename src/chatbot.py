
import os
import json
import yaml
import logging
from dotenv import load_dotenv
from .utils import fileExtensionToLoader, loadConfig, getTextChunks

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema.runnable import RunnablePassthrough

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

app = FastAPI()
config = loadConfig()
load_dotenv()

@app.post("/upload/")
async def upload(file: UploadFile = File(...), chunk=False):
    '''
    Upload a file, and add to vector database
    '''

    # @todo: incorporate chunk reading of file
    try:
        rawContent = file.file.read()                   # Byte string
        decodedContent = rawContent.decode("utf-8")     # String object
        stream = open(file.filename, "wb")
    except Exception as error:
        raise HTTPException(status_code=404, detail=error)
    finally:
        file.file.close()
        stream.close()

    # Load document and split into chunks
    docs = getTextChunks(decodedContent)

    # Create embedding function and load into Chroma
    embeddingFunction = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("API_KEY"))
    database = Chroma.from_documents(docs, embeddingFunction)
    retriever = database.as_retriever(k=10)
    return {"name": file.filename, "size": file.size, "content": decodedContent}

@app.get("/")
async def root():
    return config