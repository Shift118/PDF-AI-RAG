from dataLoader import load_documents
from splitter import split_documents
from dataBase import add_to_chroma, clear_database
from queryData import query_rag
import streamlit as st
import os

# Set up the page configuration for the Streamlit app
st.set_page_config(
    page_title="PDF AI",
    layout="centered",
    page_icon="📖"
)

# Display the title of the application
st.title("PDF AI")

# Define the folder where uploaded files will be stored
upload_folder = "data/books"

# Initialize session state for uploaded files if not already present
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = os.listdir(upload_folder)

# Initialize session state for the file uploader key if not already present
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# Function to update the file uploader key
def update_key():
    st.session_state.uploader_key += 1

# Add a header to the sidebar
st.sidebar.header("Uploaded Files")

# Create a form in the sidebar for file deletion
with st.sidebar.form("delete_form"):
    # Display the list of uploaded files in the sidebar
    if st.session_state.uploaded_files:
        for i, file in enumerate(st.session_state.uploaded_files, start=1):
            st.subheader(f"{i}) {file}")

    # Add a button to delete all files in the folder
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
            st.rerun()  # Rerun the app to reflect changes
        except Exception as e:
            st.warning(f"Can't delete files at the moment!\n{e}")

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
        uploaded_filenames = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(upload_folder, uploaded_file.name)

            # Save each uploaded file to the specified folder
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            uploaded_filenames.append(uploaded_file.name)

        # Display a spinner while processing the files
        with st.spinner("Processing and Adding to DB..."):
            # Load, split, and add documents to the database
            documents = load_documents()  # Load the documents
            chunks = split_documents(documents)  # Split documents into chunks
            add_to_chroma(chunks)  # Add the chunks to the Chroma database

            # Update session state with the newly uploaded files
            st.session_state.uploaded_files = os.listdir(upload_folder)
            update_key()  # Update the uploader key
        st.rerun()  # Rerun the app to reflect changes

    except Exception as e:
        st.warning(f"Error while uploading files: {e}")

# Create a form for user query input
with st.form("user_query_input"):
    query = st.text_input("Enter Your Question:", value="How to make an offer?")

    # Add a button to submit the query
    if st.form_submit_button("Query📩"):
        st.write(query)  # Display the user's query

        # Query the database using RAG (Retrieval-Augmented Generation)
        response, sources = query_rag(query)
        st.write(response)  # Display the response from the query

        # Display the sources of the response
        st.write("Sources📖:")
        cleaned_source = "\n".join(sorted(set([reference[11:-2].replace(":", " | Page ") for reference in sources])))
        st.text(cleaned_source)  # Display cleaned and formatted sources