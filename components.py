from config import pinecone_api_key, pinecone_index_name, llama_endpoint
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

class components:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="llama2",
            temperature=0,
            max_tokens=256,
            request_timeout=30,
            base_url=llama_endpoint,
            api_key="not-needed"
        )
        
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

        self.pc = Pinecone(api_key=pinecone_api_key)
        self.index = self.pc.Index(pinecone_index_name)
        self.vector_store = PineconeVectorStore(embedding=self.embeddings, index=self.index)