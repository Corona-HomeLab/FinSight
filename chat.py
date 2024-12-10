from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_experimental.chat_models import Llama2Chat
from langchain_community.llms import HuggingFaceTextGenInference
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

# Set up the connection to your local LLaMA 2 model
llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:5000",  # Replace with your actual endpoint
    max_new_tokens=512,
    top_k=50,
    temperature=0.1,
    repetition_penalty=1.03,
)

# Wrap the LLM with Llama2Chat
model = Llama2Chat(llm=llm)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

pc = Pinecone(api_key=...)
index = pc.Index(index_name)

vector_store = PineconeVectorStore(embedding=embeddings, index=index)