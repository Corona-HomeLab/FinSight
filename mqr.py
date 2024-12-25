from components import components
from prompts import QUERY_PROMPT, output_parser
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import logging

class MQR(components):
    def __init__(self):
        super().__init__()  # Initialize components parent class
        self.llm_chain = QUERY_PROMPT | self.llm | output_parser

    def load_and_split_document(self, url="https://lilianweng.github.io/posts/2023-06-23-agent/"):
        self.loader = WebBaseLoader(url)
        self.data = self.loader.load()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        self.splits = self.text_splitter.split_documents(self.data)

    def sample_qa(self):
        self.question = "What are the approaches to Task Decomposition?"
        self.retriever_from_llm = MultiQueryRetriever(
            retriever=self.vector_store.as_retriever(), llm_chain=self.llm_chain, parser_key="lines"
        )
        return self.retriever_from_llm
    
    def logging(self):
        logging.basicConfig()
        logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)


# Other inputs
question = "What are the approaches to Task Decomposition?"

mqr = MQR()

mqr.sample_qa()

unique_docs =  mqr.retriever_from_llm.invoke(mqr.question)
print(len(unique_docs))
