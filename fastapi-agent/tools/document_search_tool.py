import os
from langchain.tools import tool
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch

_retriever = None


def build_retriever():
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
    return vectorstore.as_retriever(search_kwargs={"k": 4})


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = build_retriever()
    return _retriever


@tool
def internal_document_search(query: str) -> str:
    """Search internal company documents for relevant information.
    Use this for questions about policies, procedures, products, or any company-specific topic.
    Input should be a natural language search query.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant documents found in the knowledge base."
    parts = [f"[Document {i + 1}]:\n{doc.page_content}" for i, doc in enumerate(docs)]
    return "\n\n---\n\n".join(parts)