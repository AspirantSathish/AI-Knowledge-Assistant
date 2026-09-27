import streamlit as st

from llm import ask_llm


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖"
)

st.title("🤖 AI Knowledge Assistant")

st.write(
    "LLM + Conversation History"
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user message
if prompt := st.chat_input("Ask a question"):

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = ask_llm(
                st.session_state.messages
            )

        st.markdown(answer)

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
    
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()