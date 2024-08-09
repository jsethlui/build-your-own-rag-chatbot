
import yaml
from fastapi import HTTPException

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document

def loadConfig():
    # @todo: if config has already been read, no need to read again
    try:
        stream = open("../config.yaml", "r")
        config = yaml.safe_load(stream)
    except yaml.YAMLError as error:
        raise HTTPException(status_code=404, detail=error)
    except IOError:
        raise HTTPException(status_code=404, detail="Cannot load config.yaml")
    finally:
        stream.close()
        return config

def fileExtensionToLoader(fileName):
    if (fileName.endswith(".pdf" )):
        return PyPDFLoader
    if (fileName.endswith(".txt")):
        return TextLoader

def getTextChunks(text, chunkSize=1000, chunkOverlap=0):
    # Load document and split into chunks
    textSplitter = CharacterTextSplitter(chunk_size=chunkSize, chunk_overlap=chunkOverlap)
    docs = [Document(page_content=splitted) for splitted in textSplitter.split_text(text)]
    return docs