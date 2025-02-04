from dataLoader import load_documents
from splitter import split_documents
from dataBase import add_to_chroma, clear_database
from queryData import query_rag
import streamlit as st
import numpy as np
import os

selected_files = []
        
# Set up the page configuration for the Streamlit app
st.set_page_config(
    page_title="PDF AI",
    layout="centered",
    page_icon="📖"
)

# Define the folder where uploaded files will be stored
upload_folder = "data/books"

#initializing arrays
uploaded_files = os.listdir(upload_folder)
existing_files = []
# Display the title of the application
st.title("PDF AI")



# Initialize session state for the file uploader key if not already present
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# Function to update the file uploader key
def update_key():
    st.session_state.uploader_key += 1

# Add a header to the sidebar
st.sidebar.header("Uploaded Files")

# Display the list of uploaded files in the sidebar
if uploaded_files != existing_files:
    existing_files = uploaded_files
    selected_files = []
    for i, file in enumerate(uploaded_files, start=1):
        if st.sidebar.checkbox(f"{i}) {file}", value= True):
            selected_files.append(file)

# Add a button to delete all files in the folder
if st.sidebar.button("Delete Selected Files🗑️"):
    if selected_files:
        try:
            # Clear the database before deleting files
            clear_database(selected_files)

            # Delete all files in the folder
            for file in selected_files:
                file_path = os.path.join(upload_folder, file)
                os.remove(file_path)
                
            st.rerun()  # Rerun the app to reflect changes
        except Exception as e:
            st.warning(f"Can't delete files at the moment!\n{e}")
    else:
        st.warning("Select a File to Delete!")

# File uploader interface to allow multiple PDF uploads
uploaded_files = st.file_uploader(
    "Upload Your PDF", 
    type=["pdf"], 
    accept_multiple_files=True, 
    key=f"uploader_{st.session_state.uploader_key}"
)

# Process uploaded files if any exist
if uploaded_files:
    try:
        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_folder, uploaded_file.name)
            # Save each uploaded file to the specified folder
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        # Display a spinner while processing the files
        with st.spinner("Processing and Adding to DB..."):
            # Load, split, and add documents to the database
            documents = load_documents()  # Load the documents
            chunks = split_documents(documents)  # Split documents into chunks
            add_to_chroma(chunks)  # Add the chunks to the Chroma database

            update_key()  # Update the uploader key
        st.rerun()  # Rerun the app to reflect changes

    except Exception as e:
        st.warning(f"Error while uploading files: {e}")

# Create a form for user query input
with st.form("user_query_input"):
    query = st.text_input("Enter Your Question:")

    # Add a button to submit the query
    if st.form_submit_button("Query with Selected Files🤖"):
        # Check if there is files selected
        if  selected_files:
            st.write(query)  # Display the user's query

            # Query the database using RAG (Retrieval-Augmented Generation)
            response, sources = query_rag(query,selected_files)
            st.write(response)  # Display the response from the query

            # Display the sources of the response
            st.write("Sources📖:")
            cleaned_source = "\n".join(sorted(set([reference[11:-2].replace(":", " | Page ") for reference in sources])))
            st.text(cleaned_source)  # Display cleaned and formatted sources
        else:
            st.warning("Select a File to Search!")