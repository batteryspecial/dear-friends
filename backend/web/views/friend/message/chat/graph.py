import os
from pprint import pprint
from django.utils.timezone import localtime, now

import lancedb
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import add_messages, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.constants import START, END
from typing import (
    TypedDict, 
    Annotated, 
    Sequence
)

from web.documents.utils.custom import CustomEmbeddings

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
            """
            查询当前的精确时间，返回格式为：年-月-日 时:分:秒
            :return str
            """
            # print("\033[1m" + "get_time() tool has been used!" + "\033[0m")
            return localtime(now()).strftime('%Y-%m-%d %H:%M:%S')

        @tool
        def search_knowledge_base(query: str) -> str:
            """
            在知识库中搜索与用户问题相关的信息，适用于任何知识库可能包含答案的问题
            :query str
            :return str
            """
            db = lancedb.connect('./web/documents/lancedb_storage')
            table = db.open_table('my_knowledge_base')
            embeddings = CustomEmbeddings()
            query_vector = embeddings.embed_query(query)
            results = (
                table.search(query_type="hybrid")
                .vector(query_vector)
                .text(query)
                .limit(5)
                .to_list()
            )
            context = '\n\n'.join([f'内容片段 | {i+1}\n{r["text"]}' for i, r in enumerate(results)])
            return f'从知识库中找到以下相关信息:\n\n{context}'


        tools = [get_time, search_knowledge_base]

        # https://reference.langchain.com/python/langchain-google-genai/chat_models/ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            thinking_budget=0,
        ).bind_tools(tools)

        system_prompt = SystemMessage(content=(
            "在拒绝回答或声称不知道之前, 必须先调用search_knowledge_base工具检查知识库, 即使问题看起来奇怪或像虚构内容。"
        ))

        def model_call(state: AgentState) -> AgentState:
            pprint(state)
            r = llm.invoke([system_prompt, *state["messages"]])
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
