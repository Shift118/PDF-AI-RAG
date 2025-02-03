from dataLoader import load_documents
from splitter import split_documents
from dataBase import add_to_chroma, clear_database
from queryData import query_rag
import streamlit as st
import os

# Setting up the page configuration
st.set_page_config(
    page_title="PDF AI",
    layout="centered",
    page_icon="📖"
)

# Title of the app
st.title("PDF AI")

# Folder for uploaded files
upload_folder = "data/books"

# Initialize session state for uploaded files if not already present
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = os.listdir(upload_folder)  # Load existing files in the folder

# Sidebar header
st.sidebar.header("Uploaded Files")

# Sidebar form for file deletion
with st.sidebar.form("delete_form"):
    # Display the uploaded files in the sidebar
    if st.session_state.uploaded_files:
        for i, file in enumerate(st.session_state.uploaded_files, start=1):
            st.subheader(f"{i}) {file}")

    # Deleting all files in the folder
    if st.form_submit_button("Delete All Files🫗"):
        try:
            # Clear the database before deleting files
            clear_database()

            # Delete all files in the folder
            for file in st.session_state.uploaded_files:
                file_path = os.path.join(upload_folder, file)
                os.remove(file_path)

            # Reset the list of uploaded files in session state
            st.session_state.uploaded_files = []
            st.success("All Files Have Been Deleted.")
        except Exception as e:
            st.warning(f"Can't delete files at the moment!\n{e}")

# File upload interface (allow multiple files)
uploaded_files = st.file_uploader("Upload Your PDF", type="pdf", accept_multiple_files=True)

# Process uploaded files if any exist
if uploaded_files:
    try:
        uploaded_filenames = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_folder, uploaded_file.name)

            # Save each uploaded file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            uploaded_filenames.append(uploaded_file.name)

        with st.spinner("Processing and Adding to DB..."):
            # Load, split, and add documents to the database for each uploaded file
            for file in uploaded_filenames:
                documents = load_documents()  # Load the documents
                chunks = split_documents(documents)  # Split documents into chunks
                add_to_chroma(chunks)  # Add the chunks to Chroma database
            
            # Update session state with the newly uploaded files
            st.session_state.uploaded_files = os.listdir(upload_folder)
            st.success(f"{len(uploaded_filenames)} Files Have Been Uploaded")

    except Exception as e:
        st.warning(f"Error while uploading files: {e}")

# Query input field for the user
query = st.text_input("Enter Your Question:", value="How to make an offer?")

# Button to submit the query
if st.button("Query📩"):
    st.write(query)
    # Query the database using RAG
    response, sources = query_rag(query)
    st.write(response)
    st.write("Sources📖:")

    # Clean and display the sources
    cleaned_source = "\n".join(sorted(set([reference[11:-2].replace(":", " | Page ") for reference in sources])))
    st.text(cleaned_source)
