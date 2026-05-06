"""
Singleton LangChain Agent using Azure OpenAI.
Created once at FastAPI startup and reused for every request.
"""
import os
import logging
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.calculator_tool import calculator
from tools.document_search_tool import internal_document_search

logger = logging.getLogger(__name__)

_agent_executor: AgentExecutor | None = None


def _build_agent() -> AgentExecutor:
    logger.info("Initialising Azure LangChain agent…")

    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        temperature=0,
        streaming=False,
    )

    tools = [calculator, internal_document_search]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are a helpful AI assistant for the company. "
                "You have access to two tools:\n"
                "1. calculator — for any arithmetic or math questions.\n"
                "2. internal_document_search — for any company-specific questions.\n"
                "Always use a tool when appropriate before answering."
            ),
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)
    logger.info("Azure LangChain agent ready.")
    return executor


def get_agent() -> AgentExecutor:
    global _agent_executor
    if _agent_executor is None:
        _agent_executor = _build_agent()
    return _agent_executor


def run_agent(question: str) -> str:
    executor = get_agent()
    result = executor.invoke({"input": question})
    return result.get("output", "No answer returned.")