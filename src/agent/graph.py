
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

from src.agent.state import AgentState
from src.agent.nodes import agent_node, HR_TOOLS


# Create the graph builder
builder = StateGraph(AgentState)

# Add agent and tools nodes
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(HR_TOOLS))

# Define the workflow
builder.add_edge(START, "agent")

# Decide whether to call a tool or finish
builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)

# Return to the agent after tool execution
builder.add_edge("tools", "agent")

# Enable conversation memory
memory = MemorySaver()

# Compile the graph
graph = builder.compile(checkpointer=memory)


if __name__ == "__main__":

    print("HR COPILOT AGENT")
    print("================")

    config = {
        "configurable": {
            "thread_id": "hr-demo-session"
        }
    }

    response = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="How many annual leave days do full-time employees receive?"
                )
            ]
        },
        config=config
    )

    print("\nAGENT RESPONSE:")
    print(response["messages"][-1].content)
