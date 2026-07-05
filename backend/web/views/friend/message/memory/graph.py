import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph, add_messages

from typing import (
    TypedDict, 
    Annotated, 
    Sequence
)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class MemoryGraph:
    @staticmethod
    def create_app():
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            thinking_budget=0,
        )

        def model_call(state: AgentState) -> AgentState:
            r = llm.invoke(state["messages"])
            return {'messages' : [r]}

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", model_call)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)

        return workflow.compile()
