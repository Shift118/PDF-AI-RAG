# OLLAMA EMBEDDING VERSION CODE
from langchain_ollama import OllamaEmbeddings

def get_embedding_function():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

# BEDROCK EMBEDDING VERSION CODE

# from langchain_community.embeddings.bedrock import BedrockEmbeddings

# def get_embedding_function():
#     embeddings = BedrockEmbeddings(
#         credentials_profile_name="defualt",
#         region_name="us-east-1"
#         )
#     return embeddings



