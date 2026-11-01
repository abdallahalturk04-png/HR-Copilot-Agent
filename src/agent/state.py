
from typing import Annotated, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """
    State shared between all nodes in the HR Copilot Agent.
    """

    # Conversation history
    messages: Annotated[list[AnyMessage], add_messages]

    # Retrieved HR policy information
    retrieved_context: str

    # Sources used to answer the question
    sources: list[dict]
