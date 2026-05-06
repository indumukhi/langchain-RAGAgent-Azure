"""
One-time script: upload PDF documents to Azure AI Search.
Place your PDFs in the ./docs/ folder, then run: python upload_docs.py
"""
import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

load_dotenv()

embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

vectorstore = AzureSearch(
    azure_search_endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    azure_search_key=os.environ["AZURE_SEARCH_KEY"],
    index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    embedding_function=embeddings.embed_query,
)
print("Connected to Azure AI Search:", os.environ["AZURE_SEARCH_INDEX_NAME"])

loader = DirectoryLoader("./docs", glob="**/*.pdf", loader_cls=PyPDFLoader)
raw_docs = loader.load()
print(f"Loaded {len(raw_docs)} document(s).")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(raw_docs)
print(f"Split into {len(chunks)} chunk(s).")

vectorstore.add_documents(chunks)
print("Upload complete!")