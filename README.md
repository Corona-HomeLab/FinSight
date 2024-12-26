# Project Overview

This project is a financial data analysis assistant designed to help users understand their financial data by answering questions about transactions and financial records. It leverages various components to load, process, and retrieve data from APIs and vector stores.

## Key Components

### 1. **MQR (Multi-Query Retriever)**
- **Purpose**: Manages API sources, processes data, and facilitates chat interactions.
- **Key Functions**:
  - `add_api_source`: Adds a new API source and loads its data.
  - `remove_api_source`: Removes an API source and its documents from the vector store.
  - `chat`: Handles user queries and retrieves relevant information.
  - `get_retriever`: Initializes a retriever with optional namespace filtering.

### 2. **APILoader**
- **Purpose**: Loads data from specified API endpoints and formats it into documents.
- **Key Functions**:
  - `load`: Fetches data from an API and converts it into a list of `Document` objects.
  - `_format_content`: Formats the content of each document based on its type.

### 3. **SourceManager**
- **Purpose**: Manages the configuration and state of API sources.
- **Key Functions**:
  - `add_source`: Adds a new API source configuration.
  - `remove_source`: Removes an existing API source.
  - `get_active_sources`: Retrieves all active sources.

### 4. **Prompts**
- **Purpose**: Defines templates for generating queries and chat responses.
- **Key Components**:
  - `QUERY_PROMPT`: Template for generating multiple versions of a user question.
  - `CHAT_PROMPT`: Template for generating responses to user queries.

### 5. **Components**
- **Purpose**: Initializes and configures the language model and vector store.
- **Key Components**:
  - `ChatOpenAI`: Configures the language model for generating responses.
  - `PineconeVectorStore`: Manages the vector store for document retrieval.

## Configuration

- **API Keys and Endpoints**: Configured in `config.py`.
- **Source Configurations**: Managed in `sources_config.json`.

## Usage

1. **Command Mode**: 
   - Add, remove, or list API sources.
   - Switch to chat mode for interactive queries.

2. **Chat Mode**: 
   - Ask questions about financial data and receive detailed responses.

## Development

- **Dependencies**: Ensure all required Python packages are installed.
- **Environment**: Configure API keys and endpoints in `config.py`.

## Security

- **Sensitive Files**: `config.py` and `sources_config.json` are included in `.gitignore` to prevent accidental exposure of sensitive information.

## Workflow

- **Bandit Security Linter**: Configured in `.github/workflows/bandit.yml` to scan for common security issues in the codebase.

## Contributing

- Contributions are welcome. Please ensure code quality and consistency with existing components.

## License

- This project is licensed under the MIT License.
