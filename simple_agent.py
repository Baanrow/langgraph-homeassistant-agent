from ha_tools import tools
from langgraph.graph import START, END, StateGraph, add_messages
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from config import llm
from langgraph.prebuilt import ToolNode

conn = sqlite3.connect("state_db/memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

class StateClass(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def graph_flow() -> StateGraph:
    """
    Builds and compiles a LangGraph workflow for tool-enabled LLM interaction.

    This function defines the graph nodes, control flow logic, and checkpoints, 
    then compiles and returns a StateGraph object. The returned graph can be invoked 
    at runtime with a state and config to process messages, handle tool calls, and 
    manage conversational flow.

    Returns:
        StateGraph: A compiled graph object ready for invocation.
    """
    llm_with_tools = llm.bind_tools(tools)
    
    def invoke_llm(state: StateClass) -> StateClass:
        """
        Invokes the LLM with state["messages"], appends the response
        to state["messages"] then returns state.

        Args:
            state (StateClass): State format.

        Returns:
            StateClass: State format.
        """
        response = llm_with_tools.invoke(state["messages"])
        state["messages"].append(response)
        
        return state
    
    def tool_decision(state: StateClass) -> str:
        """
        Takes in state and checks the last message for a "tool_calls" attribute
        which indictates that a tool call is required. Returns a relevant string
        to determine the flow of the graph.

        Args:
            state (StateClass): State format.

        Returns:
            str: Returns "toolit" if a tool call is required. Otherwise returns "END".
        """
        last_message = state["messages"][-1]
        return "toolit" if getattr(last_message, "tool_calls", None) else "END"
    
    toolbox = ToolNode(tools)
    
    graph = (
        StateGraph(StateClass)
        .add_node("llm", invoke_llm)
        .add_node("toolit", toolbox)
        .set_entry_point("llm")
        .add_edge(START, "llm")
        .add_edge("toolit", "llm")
        .add_conditional_edges("llm", tool_decision)
        .compile(checkpointer=checkpointer)
    )
    
    return graph
