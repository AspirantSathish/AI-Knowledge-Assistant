import asyncio
import streamlit as st

from orchestrator import ask_assistant


st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 AI Knowledge Assistant")

st.caption(
    "Ask questions about company policies "
    "or your employee information."
)


# -----------------------------------------
# Session state
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------------
# Sidebar
# -----------------------------------------

with st.sidebar:

    st.header("Employee")

    employee_id = st.text_input(
        "Employee ID",
        value="EMP001"
    )

    if st.button("Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# -----------------------------------------
# Display conversation
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------------------
# User input
# -----------------------------------------

question = st.chat_input(
    "Ask a question..."
)


if question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # -------------------------------------
    # Call orchestrator
    # -------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = asyncio.run(
                    ask_assistant(
                        question=question,
                        employee_id=employee_id
                    )
                )

                answer = result["answer"]

                st.markdown(answer)

            except Exception as exc:

                answer = (
                    "Sorry, I couldn't process "
                    "your request."
                )

                st.error(answer)

                # For development only
                st.exception(exc)


    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })