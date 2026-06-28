import os

from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import add_messages, StateGraph
from langgraph.constants import START, END
from typing import (
    TypedDict, 
    Annotated, 
    Sequence
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class ChatGraph:
    """
    The most basic langgraph graph.

    start -> agent -> end (3 states)
    """
    @staticmethod
    def create_app():
        # https://reference.langchain.com/python/langchain-anthropic/chat_models/ChatAnthropic
        llm = ChatAnthropic(
            model_name="claude-3-5-haiku-20241022",
            api_key=os.getenv("CLAUDE_API_KEY")
        )

        def model_call(state: AgentState) -> AgentState:
            r = llm.invoke(state["messages"])
            return {"messages" : [r]}
        
        workflow = StateGraph(state_schema=AgentState)
        workflow.add_node("agent", model_call)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        return workflow.compile()
