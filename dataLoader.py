from langchain_community.document_loaders import PyPDFDirectoryLoader

file_path = "data/books/"

def load_documents():
    try:
        document_loader = PyPDFDirectoryLoader(file_path)
        print("Loader initialized successfully.")
        documents = document_loader.load()
        print(f"Number of documents loaded: {len(documents)}")
        return documents
    except Exception as e:
        print(f"An error occurred while loading documents: {e}")
        raise