from dataLoader import load_documents 
from splitter import split_documents
from dataBase import add_to_chroma

print("Document Loading")
documents = load_documents()  # Load the documents
print("Document Splitting")
chunks = split_documents(documents)  # Split documents into chunks
print("Add to DB!✅")
add_to_chroma(chunks)  # Add the chunks to Chroma database
print("DONE✅✅✅✅")