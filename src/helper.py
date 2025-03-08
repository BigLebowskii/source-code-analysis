from git import Repo
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

#clone github repos
def repo_injestion(repo_url):
    os.makedirs("repo", exist_ok=True)
    repo_path = "repo/"
    Repo.clone_from(repo_url, to_path=repo_path)


#extract repos as documents
def load_repo(repo_path): 
    loader = GenericLoader.from_filesystem(repo_path,
    glob = "**/*",
    suffixes=[".py"],
    parser = LanguageParser(language=Language.PYTHON, parser_threshold = 500))
                    
    documents = loader.load()
    return documents

def text_splitter(documents):
    document_splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
    chunk_size= 2000,
    chunk_overlap = 200)
    text_chunks = document_splitter.split_documents(documents)
    return text_chunks

def load_embedding():
    embeddings=OpenAIEmbeddings(disallowed_special=())
    return embeddings


load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings(disallowed_special=())
                                                                 
