import streamlit as st
from ingest import process_cvs
from chat import chat_interface

# Simple navigation
PAGES = {
    "Process CVs": process_cvs,
    "Chatbot": chat_interface
}

def main():
    st.title("AI Talent Acquisition Chatbot")
    page_choice = st.sidebar.selectbox("Select Page", list(PAGES.keys()))
    page_func = PAGES[page_choice]
    page_func()

if __name__ == "__main__":
    main()
