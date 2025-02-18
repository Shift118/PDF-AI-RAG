from embedding import get_embedding_function
from langchain_chroma import Chroma
from langchain.schema.document import Document
import os

CHROMA_PATH = "chroma"

# Storing information using embeddings "vector" as a key
def add_to_chroma(chunks: list[Document]):
    # Load the existing DB
    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding_function()
    )
    try:
        # Calculate Page IDs
        chunks_with_ids = calculate_chunk_ids(chunks)

        # ADD or Update the documents
        existing_items = db.get(include=[])  # IDs are always included by default
        existing_ids = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist
        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            print(f"👉 Adding new documents: {len(new_chunks)}")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
            print(f"✅ Documents Added To Chroma")
        else:
            print("✅ No new documents to add")
    finally:
        db._client._system.stop()

def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data
        chunk.metadata["id"] = chunk_id
    return chunks

def clear_database():
    try:
        # Initialize Chroma instance
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=None
        )
        # Use delete_collection to safely clear all data
        db._client._system.start()
        db.delete_collection()
        print("✅ Database cleared successfully.")
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
