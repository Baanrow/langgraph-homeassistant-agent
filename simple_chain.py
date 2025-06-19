from simple_agent import graph_flow
from langgraph.types import StateSnapshot
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

class SimpleChain:
    def __init__(self) -> None:
        "Compile the graph"
        self.graph = graph_flow()
    
    
    def get_state_snapshot(self, config: dict) -> StateSnapshot:
        """
        Gets a snapshot of the current state using config.

        Args:
            config (dict): A dict containing the thread_id.

        Returns:
            StateSnapshot.
        """
        return self.graph.get_state(config)
    
    
    def get_state(self, state_snapshot: StateSnapshot) -> dict[str, list[BaseMessage]]:
        """
        Extracts state from state snapshot.

        Args:
            state_snapshot (StateSnapshot).

        Returns:
            dict[str, list[BaseMessage]]: State format.
        """
        return state_snapshot.values
    
    
    def convert_state_streamlit(self, state: dict[str, list[BaseMessage]]) -> list[dict[str, str]]:
        """
        Converts state["messages"] into a Streamlit-ready list of dict messages.

        Args:
            state (dict[str, list[BaseMessage]]): State format.

        Returns:
            list[dict[str, str]]: Streamlit format message structure.
        """
        st_messages = []
        for msg in state["messages"]:
            content = msg.content
            if isinstance(msg, HumanMessage):
                st_messages.append({"role": "user", "content": content})
            elif isinstance(msg, AIMessage) and content.strip():
                st_messages.append({"role": "assistant", "content": content})
        
        return st_messages
    
    
    def invoke_graph(self, state: dict[str, list[BaseMessage]], config: dict, prompt: str) -> str:
        """
        Appends the prompt to state["messages"] then invokes the graph with state and config.

        Args:
            state (dict[str, list[BaseMessage]]): State format.
            config (dict): A dict containing the thread_id.
            prompt (str): The user's prompt.

        Returns:
            str: Returns the response as a string.
        """
        state["messages"].append(HumanMessage(content=prompt))
        response = self.graph.invoke(state, config)
        
        return response["messages"][-1].content
