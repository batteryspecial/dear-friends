import os

from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
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
        # https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            thinking_budget=0,
        )

        def model_call(state: AgentState) -> AgentState:
            r = llm.invoke(state["messages"])
            return {"messages" : [r]}
        
        workflow = StateGraph(state_schema=AgentState)
        workflow.add_node("agent", model_call)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        return workflow.compile()
