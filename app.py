
import uuid
import streamlit as st

from langchain_core.messages import HumanMessage
from src.agent.graph import graph


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="HR Copilot Agent",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🤖 HR Copilot")
    st.caption("AI-Powered Human Resources Assistant")

    st.divider()

    st.markdown("### Available Features")

    st.markdown("""
    - 📚 HR Policy Search
    - 👥 Employee Database
    - 🧮 HR Calculations
    - 💬 Conversation Memory
    """)

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.rerun()

    st.caption("Powered by Ollama, LangGraph and ChromaDB")


# --------------------------------------------------
# MAIN INTERFACE
# --------------------------------------------------

st.title("HR Copilot Agent")

st.write(
    "Hello! I'm your HR assistant. "
    "Ask me about company policies, employees, "
    "leave balances, and HR calculations."
)

st.divider()


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_question = st.chat_input("Ask your HR question...")


if user_question:

    # Display user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner("HR Copilot is thinking..."):

            try:
                response = graph.invoke(
                    {
                        "messages": [
                            HumanMessage(content=user_question)
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }
                )

                answer = response["messages"][-1].content

                if not isinstance(answer, str):
                    answer = str(answer)

                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:

                st.error(
                    f"Something went wrong: {str(error)}"
                )
