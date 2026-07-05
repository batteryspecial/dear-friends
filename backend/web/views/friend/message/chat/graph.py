import os
from pprint import pprint
from django.utils.timezone import localtime, now

from langchain_core.messages import BaseMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages, StateGraph
from langgraph.constants import START, END
from typing import (
    TypedDict, 
    Annotated, 
    Sequence
)

from langgraph.prebuilt import ToolNode

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

class ChatGraph:
    """
    The most basic langgraph graph + functional tools.

    start -> agent -> condition? -> tools -> end
               ↑                      |
               |______________________|
    """
    @staticmethod
    def create_app():
        @tool
        def get_time() -> str:
            """查询当前的精确时间，返回格式为：年-月-日 时:分:秒"""
            print("\033[1m" + "get_time() tool has been used!" + "\033[0m")
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        tools = [get_time]

        # https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            thinking_budget=0,
        ).bind_tools(tools)

        def model_call(state: AgentState) -> AgentState:
            pprint(state)
            r = llm.invoke(state["messages"])
            return {"messages" : [r]}

        def can_continue(state: AgentState) -> str:
            last_message = state.get("messages")[-1]
            if last_message.tool_calls:
                return "tools"
            return "end"
        
        tool_node = ToolNode(tools)
        
        workflow = StateGraph(state_schema=AgentState)
        workflow.add_node("agent", model_call)
        workflow.add_node("tools", tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_edge("agent", END)
        workflow.add_conditional_edges("agent", can_continue, path_map={
            'tools': 'tools',
            'end': END
        })
        workflow.add_edge("tools", "agent")

        return workflow.compile()
