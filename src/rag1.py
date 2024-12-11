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
import torch
from prompts import PROMPT_TEMPLATES

class RAG:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=llama_endpoint,
            temperature=0,
            max_tokens=512,
            request_timeout=120,
            base_url=llama_endpoint,
            api_key="not-needed"
        )
        
        # Initialize embeddings with GPU support
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cuda'} if torch.cuda.is_available() else {'device': 'cpu'}
        )
        
        # Fixed Pinecone initialization
        pc = Pinecone(api_key=pinecone_api_key)
        index = pc.Index(pinecone_index_name)
        self.vector_store = PineconeVectorStore(
            embedding=self.embeddings,
            index=index
        )
        
        self.prompt_templates = PROMPT_TEMPLATES
        self.current_data_type = "transactions"

    def set_data_type(self, data_type: str):
        """Set the type of data being analyzed to use appropriate prompt"""
        if data_type in self.prompt_templates:
            self.current_data_type = data_type
        else:
            self.current_data_type = "default"

    def index_data(self, json_data: str):
        """Index JSON data into vector store using RecursiveJsonSplitter"""
        # Parse JSON data
        data = json.loads(json_data)
        
        # Initialize RecursiveJsonSplitter with basic parameters
        splitter = RecursiveJsonSplitter(
            max_chunk_size=500,
            min_chunk_size=100,
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
        """Create the RAG chain with data-specific prompt"""
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        template = self.prompt_templates[self.current_data_type]
        prompt = PromptTemplate.from_template(template)
        
        chain = (
            {"context": retriever, "question": RunnablePassthrough()} 
            | prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        return chain

    def query(self, question: str) -> str:
        """Query the RAG system with improved timeout handling"""
        try:
            chain = self.create_chain()
            # Add timeout handling and retry logic
            for attempt in range(3):  # Try up to 3 times
                try:
                    response = chain.invoke(
                        question,
                        config={
                            "callbacks": None,
                            "run_name": None,
                            "timeout": 120  # Match the request_timeout
                        }
                    )
                    return response.strip() if response else "No response received"
                except TimeoutError:
                    if attempt == 2:  # Last attempt
                        return "Request timed out after multiple attempts"
                    continue  # Try again
            
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
        rag.set_data_type("transactions")  # Set appropriate data type
        rag.index_data(json_data)
        
        print("\nFinancial Analysis System Ready!")
        print("--------------------------------")
        
        # Interactive query loop
        while True:
            question = input("\nEnter your question (or 'quit' to exit): ")
            if question.lower() == 'quit':
                break
                
            print("\nProcessing query...")
            answer = rag.query(question)
            print("\nAnswer:")
            print("-------")
            print(answer)
            print("-------")
            
    except Exception as e:
        print(f"Application error: {str(e)}")    