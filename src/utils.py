
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.document import Document

def getTextChunks(text, chunkSize=1000, chunkOverlap=0):
    # Load document and split into chunks
    textSplitter = CharacterTextSplitter(chunk_size=chunkSize, chunk_overlap=chunkOverlap)
    docs = [Document(page_content=splitted) for splitted in textSplitter.split_text(text)]
    return docs