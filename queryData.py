from embedding import get_embedding_function
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import argparse

CHROMA_PATH = "chroma" 
PROMPT_TEMPLATE = """
    Answer the question based only on the following context:
    {context}
    
    ---
    Anser the question based on the above context: {question}
    """
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str,help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)
    
    
def query_rag(query_text: str,selected_files):
    embedding_function = get_embedding_function()
    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function= embedding_function
    )
    search_files_paths = [f"data\\books\\{name}" for name in selected_files]
    #Search the DB
    results = db.similarity_search_with_score(
        query_text,
        k=15,
        filter = {
            "source": {
                "$in": search_files_paths
            }
        }
        )
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc,_score in results])
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context = context_text,question=query_text)
    
    model = OllamaLLM(model="llama3.2:1b")
    response_text = model.invoke(prompt)
    
    sources = [doc.metadata.get("id",None) for doc,_score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text,sources
    
if __name__ == "__main__":
    main()