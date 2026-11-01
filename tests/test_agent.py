
from langchain_core.messages import HumanMessage

from src.agent.graph import graph


def test_agent_answers_annual_leave_question():

    config = {
        "configurable": {
            "thread_id": "test-annual-leave"
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

    answer = response["messages"][-1].content

    assert isinstance(answer, str)
    assert len(answer) > 0
    assert "21" in answer
    assert "leave" in answer.lower()
