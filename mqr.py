from components import components
from prompts import QUERY_PROMPT, output_parser, CHAT_PROMPT
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import logging
import string
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
import requests
from source_manager import SourceManager

class APILoader(BaseLoader):
    def __init__(self, endpoint, params=None, headers=None, data_key=None, data_type=None, 
                 base_url=None, username=None, user_id=None):
        self.endpoint = endpoint
        self.params = params or {}
        self.headers = headers or {}
        self.data_key = data_key
        self.data_type = data_type
        self.base_url = base_url
        self.username = username
        self.user_id = user_id
    
    def load(self) -> list[Document]:
        response = requests.get(self.endpoint, params=self.params, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        if self.data_key:
            data = data[self.data_key]
            
        if isinstance(data, list):
            documents = []
            for item in data:
                content, metadata = self._format_content(item)
                documents.append(Document(page_content=content, metadata=metadata))
            logging.info(f"Created {len(documents)} {self.data_type} documents")
            return documents
        else:
            content, metadata = self._format_content(data)
            return [Document(page_content=content, metadata=metadata)]
    
    def _format_content(self, item):
        """Format content based on data type and structure"""
        if isinstance(item, dict):
            if 'username' in item:
                # User record formatting remains the same
                metadata = {
                    "type": "user",
                    "data_type": "user",
                    "user_id": str(item.get('id', '')),
                    "username": item['username'].lower(),
                }
                content = f"User {item['username']} with ID {item.get('id', '')}"
                
            elif any(key in item for key in ['amount', 'transaction_id', 'user_id']):
                # Use the configured username instead of fetching it
                metadata = {
                    "type": "transaction",
                    "data_type": "transaction",
                    "user_id": str(item.get('user_id', '')),
                    "username": self.username,  # Use configured username
                    "transaction_id": str(item.get('id', '')),
                    "category": item.get('category', ''),
                    "amount": str(item.get('amount', 0)),
                    "date": item.get('date', '').split('T')[0],
                    "merchant": item.get('name', ''),
                    "transaction_type": "credit" if item.get('amount', 0) < 0 else "debit"
                }
                
                content = (
                    f"A {metadata['transaction_type']} transaction of ${abs(float(metadata['amount']))} "
                    f"by {self.username if self.username else f'user {metadata["user_id"]}'} "
                    f"at {metadata['merchant']} on {metadata['date']} "
                    f"in the {metadata['category'].replace('_', ' ').title()} category."
                )
        else:
            metadata = {"type": "unknown", "data_type": "unknown"}
            content = str(item)
        
        return content, metadata

    def _get_username_for_user_id(self, user_id: str) -> str:
        """Helper method to get username for a given user_id"""
        try:
            # Assuming you have access to the users data
            # This could be from a cache, database, or API call
            response = requests.get(f"{self.base_url}/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('username', '')
        except Exception as e:
            logging.error(f"Error fetching username for user_id {user_id}: {str(e)}")
        return ''

class MQR(components):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)  # Set logging level at initialization
        super().__init__()
        self.llm_chain = QUERY_PROMPT | self.llm | output_parser
        self.chat_chain = CHAT_PROMPT | self.llm
        self.chat_history = []
        self.source_manager = SourceManager()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        self.data_types = set()  # Track available types of financial data
    
    def add_api_source(self, source_id: str, config: dict) -> bool:
        """Add a new API source and load its data"""
        try:
            source = self.source_manager.add_source(source_id, config)
            endpoint_parts = str(source.endpoint).split('/')
            base_url = f"{endpoint_parts[0]}//{endpoint_parts[2]}"
            
            loader = APILoader(
                endpoint=str(source.endpoint),
                params=source.params,
                headers=source.headers,
                data_key=source.data_key,
                data_type=config.get('data_type', 'general'),
                base_url=base_url,
                username=config.get('username'),
                user_id=config.get('user_id')
            )
            documents = loader.load()
            self.data_types.add(config.get('data_type', 'general'))
            
            # Use different chunking strategies based on data type
            if config.get('data_type') == 'transactions':
                # For transactions, keep them as individual documents but add a summary document
                transactions_by_user = {}
                for doc in documents:
                    username = doc.metadata.get('username')
                    if username:
                        if username not in transactions_by_user:
                            transactions_by_user[username] = []
                        transactions_by_user[username].append(doc)
                
                # Create summary documents for each user
                summary_docs = []
                for username, user_docs in transactions_by_user.items():
                    total_debit = sum(float(d.metadata['amount']) for d in user_docs if d.metadata['transaction_type'] == 'debit')
                    total_credit = sum(float(d.metadata['amount']) for d in user_docs if d.metadata['transaction_type'] == 'credit')
                    
                    summary_content = (
                        f"Transaction summary for {username}: "
                        f"Total of {len(user_docs)} transactions. "
                        f"Total debits: ${total_debit:.2f}. "
                        f"Total credits: ${total_credit:.2f}. "
                        f"Net change: ${(total_debit + total_credit):.2f}"
                    )
                    
                    summary_docs.append(Document(
                        page_content=summary_content,
                        metadata={
                            'type': 'transaction_summary',
                            'data_type': 'transaction_summary',
                            'username': username,
                            'source_id': source_id,
                            'namespace': source.namespace
                        }
                    ))
                
                documents.extend(summary_docs)
            else:
                # Use regular text splitting for other document types
                documents = self.text_splitter.split_documents(documents)
            
            # Split documents before adding to vector store
            split_docs = self.text_splitter.split_documents(documents)
            
            # Add source_id and namespace to metadata for each document
            for doc in split_docs:
                doc.metadata['source_id'] = source_id
                doc.metadata['data_type'] = config.get('data_type', 'general')
                doc.metadata['namespace'] = source.namespace
                # Ensure username is never null in metadata
                if 'username' in doc.metadata and doc.metadata['username'] is None:
                    doc.metadata['username'] = config.get('username', 'unknown')
            
            # Add documents to vector store with custom namespace
            try:
                ids = self.vector_store.add_documents(
                    documents=split_docs,
                    namespace=source.namespace
                )
                # Store document IDs in source config
                source.document_ids = ids
                self.source_manager._save_sources()
                return True
            except Exception as e:
                logging.error(f"Error adding documents to vector store: {str(e)}")
                return False
            
        except Exception as e:
            logging.error(f"Error adding source {source_id}: {str(e)}")
            return False
    
    def remove_api_source(self, source_id: str):
        """Remove an API source and its documents from the vector store"""
        try:
            source = self.source_manager.sources.get(source_id)
            if source:
                # Delete entire namespace from Pinecone
                try:
                    logging.info(f"Deleting namespace {source.namespace} from vector store")
                    self.vector_store.delete(
                        namespace=source.namespace,
                        delete_all=True
                    )
                except Exception as e:
                    # Log the error but continue with source removal
                    logging.warning(f"Could not delete namespace {source.namespace}: {str(e)}")
                    logging.warning("Continuing with source removal...")
                
                # Remove the source completely
                logging.info(f"Removing source {source_id}")
                self.source_manager.remove_source(source_id)
                print(f"Source {source_id} removed successfully")
            else:
                logging.warning(f"Source {source_id} not found")
                print(f"Source {source_id} not found")
        except Exception as e:
            logging.error(f"Error removing source {source_id}: {str(e)}")
            print(f"Error removing source {source_id}")

    def get_retriever(self, namespaces=None):
        """Get retriever with optional namespace filtering"""
        logging.info("Initializing retriever...")
        try:
            if namespaces:
                # Add debug logging for namespace content
                for namespace in namespaces:
                    try:
                        # Test vector store content
                        doc_count = self.vector_store.similarity_search(
                            "test",
                            k=1,
                            namespace=namespace
                        )
                        logging.info(f"Namespace {namespace} contains {len(doc_count)} searchable documents")
                    except Exception as e:
                        logging.error(f"Error checking namespace {namespace}: {str(e)}")

            retriever = self.vector_store.as_retriever(
                search_type="similarity"
            )
            
            logging.info(f"Created retriever for namespace: {namespaces[0] if namespaces else 'all'}")
            return retriever
        except Exception as e:
            logging.error(f"Error creating retriever: {str(e)}")
            raise

    def chat(self, question: str) -> str:
        try:
            # Extract username and determine if it's a user query
            username = None
            question_lower = question.lower()
            is_user_query = any(keyword in question_lower for keyword in ['users', 'user', 'who'])
            
            if not is_user_query:
                # Only try to extract username if it's not a user query
                words = question_lower.translate(str.maketrans('', '', string.punctuation)).split()
                for word in words:
                    if word not in ['transactions', 'for', 'any', 'the', 'what', 'are', 'there', 'summary', 
                                  'categories', 'can', 'you', 'see', 'of', 'in', 'by', 'from']:
                        for source in self.source_manager.get_active_sources().values():
                            if source.username and word == source.username.lower():
                                username = source.username
                                break
                    if username:
                        break

            relevant_namespaces = self._get_relevant_namespaces(question, username)
            if not relevant_namespaces:
                return "I couldn't find any data for that user. Please verify the username and try again."
            
            logging.info(f"Searching in namespaces: {relevant_namespaces}")
            
            all_results = []
            for namespace in relevant_namespaces:
                try:
                    # Set filter conditions based on query type
                    if is_user_query:
                        filter_conditions = {"type": "user"}
                    else:
                        filter_conditions = {
                            "type": "transaction",
                            "username": username.lower() if username else None
                        }
                    
                    logging.info(f"Searching namespace {namespace} with filters: {filter_conditions}")
                    
                    results = self.vector_store.similarity_search(
                        question,
                        k=50,
                        namespace=namespace,
                        filter=filter_conditions
                    )
                    
                    logging.info(f"Found {len(results)} documents in {namespace}")
                    all_results.extend(results)
                    
                except Exception as e:
                    logging.error(f"Error searching namespace {namespace}: {str(e)}")
                    continue
            
            if not all_results:
                return "I couldn't find any relevant information in the database. Please verify the data has been properly loaded."
            
            # Format context from retrieved documents
            context = "\n".join(f"Document from {doc.metadata.get('namespace', 'unknown')}: {doc.page_content}" 
                              for doc in all_results)
            
            logging.info(f"Total context length: {len(context)}")
            logging.info(f"Context preview: {context[:200]}")
            
            response = self.chat_chain.invoke({
                "context": context,
                "question": question,
                "chat_history": "\n".join([f"Human: {q}\nAssistant: {a}" 
                                         for q, a in self.chat_history])
            })
            
            return response.content if hasattr(response, 'content') else str(response)
            
        except Exception as e:
            logging.error(f"Error in chat: {str(e)}")
            return "I encountered an error while processing your question. Please try again."

    def logging(self):
        logging.basicConfig()
        logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)

    def _save_sources(self):
        """Save sources config after updating document IDs"""
        try:
            self.source_manager._save_sources()
            logging.info("Sources config saved successfully")
        except Exception as e:
            logging.error(f"Error saving sources config: {str(e)}")

    def _get_relevant_namespaces(self, question: str, username: str = None) -> list[str]:
        """Determine which namespaces are most relevant to the question"""
        sources = self.source_manager.get_active_sources()
        question_lower = question.lower()
        relevant_namespaces = []
        
        # Check if this is a user-related query
        user_keywords = ['users', 'user', 'who']
        is_user_query = any(keyword in question_lower for keyword in user_keywords)
        
        if is_user_query:
            # For user queries, include the users namespace
            for source in sources.values():
                if source.data_type == 'users' or source.namespace == 'users':
                    relevant_namespaces.append(source.namespace)
        elif username:
            # For user-specific transaction queries
            for source in sources.values():
                if source.username and source.username.lower() == username.lower():
                    relevant_namespaces.append(source.namespace)
        
        logging.info(f"Selected namespaces for query: {relevant_namespaces}")
        return relevant_namespaces

def main():
    mqr = MQR()
    mode = "command"  # Start in command mode
    
    print("\nWelcome! Type 'help' for available commands.")
    
    while True:
        if mode == "command":
            command = input("\nEnter command (chat/add/remove/list/help/exit): ").strip().lower()
            
            if command == 'exit':
                print("Goodbye!")
                break
                
            elif command == 'help':
                print("\nAvailable commands:")
                print("- chat: Switch to chat mode")
                print("- add: Add a new API source")
                print("- remove: Remove an API source")
                print("- list: List active sources")
                print("- help: Show this help message")
                print("- exit: Exit the program")
                
            elif command == 'chat':
                mode = "chat"
                print("\nEntering chat mode. Type 'back' to return to command mode.")
                continue
                
            elif command == 'add':
                source_id = input("Enter source ID: ").strip()
                endpoint = input("Enter API endpoint: ").strip()
                description = input("Enter description: ").strip()
                namespace = input("Enter namespace (press enter to use source ID): ").strip() or source_id
                data_key = input("Enter data key (optional): ").strip() or None
                data_type = input("Enter data type (or press enter for general): ").strip() or "general"
                username = input("Enter username (optional): ").strip() or None
                user_id = input("Enter user ID (optional): ").strip() or None
                
                if not endpoint:
                    print("Error: API endpoint cannot be empty")
                    continue
                
                config = {
                    "name": source_id,
                    "endpoint": endpoint,
                    "description": description,
                    "namespace": namespace,
                    "data_key": data_key,
                    "data_type": data_type,
                    "username": username,
                    "user_id": user_id
                }
                
                if mqr.add_api_source(source_id, config):
                    print(f"Source {source_id} added successfully!")
                else:
                    print(f"Failed to add source {source_id}")
                    
            elif command == 'remove':
                source_id = input("Enter source ID to remove: ").strip()
                mqr.remove_api_source(source_id)
                print(f"Source {source_id} removed")
                
            elif command == 'list':
                sources = mqr.source_manager.get_active_sources()
                print("\nActive Sources:")
                if not sources:
                    print("No active sources")
                for id, source in sources.items():
                    print(f"- {id}: {source.description} ({source.endpoint})")
        
        else:  # Chat mode
            question = input("\nYour question (or 'back' to return to command mode): ").strip()
            
            if question.lower() == 'back':
                mode = "command"
                continue
            
            print("\nAnswer:", mqr.chat(question))

if __name__ == "__main__":
    main()
