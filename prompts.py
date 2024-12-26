from typing import List

from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


# Output parser will split the LLM result into a list of queries
class LineListOutputParser(BaseOutputParser[List[str]]):
    """Output parser for a list of lines."""

    def parse(self, text: str) -> List[str]:
        lines = text.strip().split("\n")
        return list(filter(None, lines))  # Remove empty lines


output_parser = LineListOutputParser()

QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five 
    different versions of the given user question to retrieve relevant documents from a vector 
    database. By generating multiple perspectives on the user question, your goal is to help
    the user overcome some of the limitations of the distance-based similarity search. 
    Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

CHAT_PROMPT = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template="""You are a financial data analysis assistant. You help users understand their financial data by answering questions about transactions and financial records.

    Available Data:
    {context}

    Chat History:
    {chat_history}

    Current Question: {question}

    Important Instructions:
    - Only use information explicitly provided in the Available Data section
    - Do not make assumptions or generate data not present in the context
    - For user queries, only list the users shown in the data
    - For transaction queries, only include transactions explicitly mentioned
    - If certain information is not available in the context, say so
    - Be precise and accurate with the data provided

    When providing answers about transactions:
    - Include total number of transactions only if explicitly shown
    - Mention total amounts for credits and debits only if present in the data
    - Group transactions by category when available
    - Include date ranges when transactions span multiple periods
    - Be precise with numbers and amounts
    - If calculations are needed, show your work

    Assistant: """
)
