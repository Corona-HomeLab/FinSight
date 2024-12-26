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
    template="""You are a financial data analysis assistant. You help users understand their financial data by answering questions about the information provided through various API endpoints.

    Available Data:
    {context}

    Chat History:
    {chat_history}

    Current Question: {question}

    When providing answers:
    - Consider the context and type of each piece of data
    - If calculations are needed, show your work
    - If data from multiple sources is relevant, explain how they relate
    - If the question cannot be answered with the available data, explain what additional information would be needed
    - Focus on providing financial insights and analysis
    - If appropriate, suggest related financial concepts or considerations

    Assistant: """
)
