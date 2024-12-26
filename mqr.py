from components import components
from prompts import QUERY_PROMPT, output_parser, CHAT_PROMPT
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import logging
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document
import requests
from source_manager import SourceManager

class APILoader(BaseLoader):
    def __init__(self, endpoint, params=None, headers=None, data_key=None, data_type=None):
        self.endpoint = endpoint
        self.params = params or {}
        self.headers = headers or {}
        self.data_key = data_key
        self.data_type = data_type  # New field to specify type of financial data
    
    def load(self) -> list[Document]:
        response = requests.get(self.endpoint, params=self.params, headers=self.headers)
        response.raise_for_status()
        
        data = response.json()
        if self.data_key:
            data = data[self.data_key]
            
        if isinstance(data, list):
            documents = []
            for item in data:
                content = self._format_content(item)
                documents.append(Document(page_content=content, metadata={"type": self.data_type}))
            logging.info(f"Created {len(documents)} {self.data_type} documents")
            return documents
        else:
            return [Document(page_content=str(data), metadata={"type": self.data_type})]
    
    def _format_content(self, item):
        """Format content based on data type and structure"""
        content_lines = []
        
        # Handle dictionary data
        if isinstance(item, dict):
            # First, try to identify if this is a user record
            if 'username' in item:
                content_lines.extend([
                    "Record Type: User",
                    f"Username: {item['username']}",
                    *[f"{k.title()}: {v}" for k, v in item.items() if k != 'username']
                ])
            # Handle financial records
            elif any(key in item for key in ['amount', 'balance', 'value']):
                content_lines.extend([
                    "Record Type: Financial",
                    *[f"{k.title()}: {'$' + str(v) if k in ['amount', 'balance', 'value'] else v}"
                      for k, v in item.items()]
                ])
            # Handle any other type of record
            else:
                content_lines.extend([
                    f"{k.title()}: {v}" for k, v in item.items()
                    if not k.startswith('_')
                ])
        else:
            content_lines.append(str(item))
        
        return "\n".join(content_lines)

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
            loader = APILoader(
                endpoint=str(source.endpoint),
                params=source.params,
                headers=source.headers,
                data_key=source.data_key,
                data_type=config.get('data_type', 'general')
            )
            documents = loader.load()
            self.data_types.add(config.get('data_type', 'general'))
            
            # Split documents before adding to vector store
            split_docs = self.text_splitter.split_documents(documents)
            
            # Add source_id and namespace to metadata for each document
            for doc in split_docs:
                doc.metadata['source_id'] = source_id
                doc.metadata['data_type'] = config.get('data_type', 'general')
                doc.metadata['namespace'] = source.namespace
            
            # Add documents to vector store with custom namespace
            try:
                ids = self.vector_store.add_documents(
                    documents=split_docs,
                    namespace=source.namespace  # Use the custom namespace
                )
                # Store document IDs in source config
                self.source_manager.sources[source_id].document_ids = ids
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
        # Log vector store state
        logging.info("Initializing retriever...")
        try:
            # Convert list of namespaces to single namespace if only one exists
            search_kwargs = {}
            if namespaces:
                if len(namespaces) == 1:
                    search_kwargs["namespace"] = namespaces[0]
                else:
                    # For multiple namespaces, we'll need to search them one by one
                    # and combine results, as Pinecone doesn't support multiple namespaces
                    # in a single query
                    search_kwargs["namespace"] = namespaces[0]  # Start with first namespace
            
            retriever = self.vector_store.as_retriever(
                search_kwargs=search_kwargs
            )
            logging.info("Successfully created base retriever")
            
            self.retriever_from_llm = MultiQueryRetriever(
                retriever=retriever,
                llm_chain=self.llm_chain,
                parser_key="lines"
            )
            logging.info("Successfully created MultiQueryRetriever")
        except Exception as e:
            logging.error(f"Error creating retriever: {str(e)}")
            raise
        return self.retriever_from_llm

    def chat(self, question: str) -> str:
        """Process a chat question using the vector store for context"""
        try:
            # Determine relevant namespaces for the question
            relevant_namespaces = self._get_relevant_namespaces(question)
            logging.info(f"Searching in namespaces: {relevant_namespaces}")
            
            # Get documents from all relevant namespaces
            all_results = []
            for namespace in relevant_namespaces:
                retriever = self.get_retriever(namespaces=[namespace])
                results = retriever.get_relevant_documents(question)
                all_results.extend(results)
            
            # Extract username if asking about specific user's transactions
            username_match = None
            question_lower = question.lower()
            if "transactions" in question_lower or "transaction" in question_lower:
                # Look for common name patterns in the question
                words = question_lower.split()
                for word in words:
                    if word not in ['transactions', 'for', 'any', 'the', 'what', 'are', 'there']:
                        username_match = word
                        break
            
            if username_match:
                # First, verify if this user exists
                user_exists = False
                user_transactions = []
                
                for doc in all_results:
                    try:
                        if isinstance(doc.page_content, str):
                            if doc.metadata.get('data_type') == 'user':
                                # Check user documents
                                if username_match in doc.page_content.lower():
                                    user_exists = True
                            elif doc.metadata.get('data_type') in ['transactions', 'financial']:
                                # Store potential transactions
                                if username_match in doc.page_content.lower():
                                    user_transactions.append(doc.page_content)
                    except:
                        continue
                
                # Format response based on findings
                if not user_exists:
                    context = f"I could not find any user with the name '{username_match}' in the system."
                elif not user_transactions:
                    context = f"While {username_match} is a user in the system, I could not find any transactions for them."
                else:
                    context = f"Found the following transactions for {username_match}:\n" + "\n".join(user_transactions)
            else:
                # Default handling for non-user-specific queries
                context = "\n".join(doc.page_content for doc in all_results)
            
            response = self.chat_chain.invoke({
                "context": context,
                "question": question,
                "chat_history": "\n".join([f"Human: {q}\nAssistant: {a}" 
                                         for q, a in self.chat_history])
            })
            
            if hasattr(response, 'content'):
                response_text = response.content
            else:
                response_text = str(response)
            
            self.chat_history.append((question, response_text))
            return response_text
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

    def _get_relevant_namespaces(self, question: str) -> list[str]:
        """Determine which namespaces are most relevant to the question"""
        # Get all active sources
        sources = self.source_manager.get_active_sources()
        
        # If question contains specific data type keywords, prioritize those namespaces
        question_lower = question.lower()
        relevant_namespaces = []
        
        # Check for transaction-related queries
        if any(word in question_lower for word in ['transaction', 'transactions', 'payment', 'payments']):
            # For user-specific transaction queries, we need both user and transaction namespaces
            words = question_lower.split()
            for word in words:
                if word not in ['transactions', 'for', 'any', 'the', 'what', 'are', 'there']:
                    # Potential username found, include both user and transaction namespaces
                    relevant_namespaces.extend(
                        source.namespace for source in sources.values()
                        if source.data_type in ['user', 'users', 'transactions', 'financial', 'general']
                    )
                    break
            # If no specific user mentioned, just include transaction namespaces
            if not relevant_namespaces:
                relevant_namespaces.extend(
                    source.namespace for source in sources.values()
                    if source.data_type in ['transactions', 'financial', 'general']
                )
        
        # Check for user-related queries
        elif any(word in question_lower for word in ['user', 'users', 'name', 'names']):
            relevant_namespaces.extend(
                source.namespace for source in sources.values()
                if source.data_type in ['user', 'users', 'general']
            )
        
        # If no specific type matches, use all active sources
        if not relevant_namespaces:
            relevant_namespaces = [source.namespace for source in sources.values()]
        
        logging.info(f"Selected namespaces for query: {relevant_namespaces}")
        return list(set(relevant_namespaces))  # Remove duplicates

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
                
                if not endpoint:
                    print("Error: API endpoint cannot be empty")
                    continue
                
                config = {
                    "name": source_id,
                    "endpoint": endpoint,
                    "description": description,
                    "namespace": namespace,
                    "data_key": data_key,
                    "data_type": data_type
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
