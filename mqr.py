from components import components
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import logging

class MQR(components):
    def __init__(self):
        super().__init__()  # Initialize components parent class

    def load_and_split_document(self, url="https://lilianweng.github.io/posts/2023-06-23-agent/"):
        self.loader = WebBaseLoader(url)
        self.data = self.loader.load()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        self.splits = self.text_splitter.split_documents(self.data)

    def sample_qa(self):
        self.question = "What are the approaches to Task Decomposition?"
        self.retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=self.vector_store.as_retriever(), llm=self.llm
        )
        return self.retriever_from_llm
    
    def logging(self):
        logging.basicConfig()
        logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)


mqr = MQR()

mqr.sample_qa()

unique_docs =  mqr.retriever_from_llm.invoke(mqr.question)
print(len(unique_docs))
