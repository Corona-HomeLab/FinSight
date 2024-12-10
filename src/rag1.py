from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from typing import List, TypedDict
from langchain_core.documents import Document
from config import pinecone_api_key, pinecone_index_name, llama_endpoint, pattern_api_endpoint
import json
import requests

class RAG:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=llama_endpoint,
            temperature=0,
            max_tokens=512,
            base_url=llama_endpoint,
            api_key="not-needed"
        )
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Fixed Pinecone initialization
        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index(pinecone_index_name)
        self.vector_store = PineconeVectorStore(
            embedding=self.embeddings,
            index=index
        )

    def index_data(self, json_data: str):
        """Index JSON data into vector store using RecursiveJsonSplitter"""
        # Parse JSON data
        data = json.loads(json_data)
        
        # Initialize RecursiveJsonSplitter with basic parameters
        splitter = RecursiveJsonSplitter(
            max_chunk_size=1000,
            min_chunk_size=200
        )
        
        # Split the JSON data
        chunks = splitter.split_text(json_data=data, convert_lists=True)
        
        # Create documents from chunks
        documents = [
            Document(
                page_content=chunk,
                metadata={"source": "transactions"}
            ) for chunk in chunks
        ]
        
        # Add to vector store
        self.vector_store.add_documents(documents=documents)

    def create_chain(self):
        """Create the RAG chain with improved prompt"""
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
        )
        
        template = """You are a helpful financial assistant. Use the following pieces of transaction data to answer the question. If you cannot answer the question based on the provided data, say "I cannot answer this based on the available information."

Context:
{context}

Question: {question}
Answer: """
        
        prompt = PromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        return chain

    def query(self, question: str) -> str:
        """Query the RAG system with error handling"""
        try:
            chain = self.create_chain()
            response = chain.invoke(question)
            return response
        except Exception as e:
            return f"An error occurred: {str(e)}"

    def get_pattern_data(self) -> str:
        """Fetch JSON data from Pattern API endpoint"""
        try:
            response = requests.get(pattern_api_endpoint)
            response.raise_for_status()  # Raise exception for bad status codes
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data from Pattern API: {str(e)}")

# Example usage
if __name__ == "__main__":
    try:
        # Initialize RAG
        rag = RAG()
        
        # Fetch and index data from Pattern API
        json_data = rag.get_pattern_data()
        rag.index_data(json_data)
        
        # Interactive query loop
        while True:
            question = input("\nEnter your question (or 'quit' to exit): ")
            if question.lower() == 'quit':
                break
                
            answer = rag.query(question)
            print(f"\nAnswer: {answer}")
            
    except Exception as e:
        print(f"Application error: {str(e)}")    