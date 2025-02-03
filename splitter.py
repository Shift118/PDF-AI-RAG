from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
'''
Chunk size is the maximum number of characters that a chunk can contain.
Chunk overlap is the number of characters that should overlap between two adjacent chunks.

The chunk size and chunk overlap parameters can be used to control the granularity of the text splitting. A smaller chunk size will result in more chunks, while a larger chunk size will result in fewer chunks. A larger chunk overlap will result in more chunks sharing common characters, while a smaller chunk overlap will result in fewer chunks sharing common characters.

use a small chunk size for tasks that require a fine-grained view of the text and a larger chunk size for tasks that require a more holistic view of the text.
'''

def split_documents (documents: list[Document]):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 800,
            chunk_overlap = 80,
            length_function = len,
            is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    except Exception as e:
        print(f"An error occurred while splitting documents: {e}")
        raise