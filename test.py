import streamlit as st

uploaded_files = ["file1","file2","file3","file4"]


import streamlit as st

uploaded_files = ["file1","file2","file3","file4"]
existing_files = []

if uploaded_files != existing_files:
    existing_files = uploaded_files
    print("exist = new")
    for file in uploaded_files:
        if st.sidebar.checkbox(f"{file}", value=True):
            print(file)