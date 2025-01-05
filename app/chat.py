import streamlit as st
from retriever import retrieve_relevant_chunks
from ollama import chat  # Import the Ollama chat function

def call_llm(context: str, query: str) -> str:
    """
    Call Ollama's Llama 3.2 model with the provided context and query.
    """
    try:
        # Combine context and query to form the input
        messages = [
            {'role': 'system', 'content': f"The following is the context:\n{context}"},
            {'role': 'user', 'content': query}
        ]

        # Call Ollama's chat function
        response = chat(model='llama3.2', messages=messages)
        return response.message.content  # Extract the content from the response

    except Exception as e:
        return f"Error: {str(e)}"

def chat_interface():
    st.header("Talent Acquisition Chatbot")

    # Persistent chat session
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    user_query = st.text_input("Ask about candidate skills, experience, etc.")

    if st.button("Send"):
        if user_query.strip():
            # 1. Retrieve relevant chunks
            chunks = retrieve_relevant_chunks(user_query, top_k=5)
            context = "\n".join(chunks)

            # 2. Call LLM with the retrieved context
            response = call_llm(context, user_query)

            # 3. Store conversation
            st.session_state["messages"].append(("user", user_query))
            st.session_state["messages"].append(("assistant", response))

    # Display chat messages
    for role, msg in st.session_state["messages"]:
        if role == "user":
            st.write(f"**User:** {msg}")
        else:
            st.write(f"**Assistant:** {msg}")

