from simple_chain import SimpleChain
import streamlit as st

config = {"configurable": {"thread_id": "1840"}}

def initialize_chain():
    if "chain" not in st.session_state:
        st.session_state["chain"] = SimpleChain()


def main():
    # Initialize the chain and create a shortcut
    initialize_chain()
    chain = st.session_state["chain"]
    
    # Get a state snapshot
    state_snapshot = chain.get_state_snapshot(config)
    
    # Get state
    state = chain.get_state(state_snapshot)
    if "messages" not in state:
        state["messages"] = []
    
    # Convert the messages to Streamlit format
    st_messages = chain.convert_state_streamlit(state)
    
    # Set session messages and create shortcut
    st.session_state["messages"] = st_messages
    messages = st.session_state["messages"]
    
    # Create the UI
    st.title("Agent Title")
    
    # Write current messages to the UI
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        with st.chat_message(role):
            st.write(content)
    
    # Prompt the user and process the response
    if prompt := st.chat_input("enter your prompt..."):
        with st.chat_message("user"):
            st.write(prompt)
        messages.append({"role": "user", "content": prompt})
        
        response = chain.invoke_graph(state, config, prompt)
        
        with st.chat_message("assistant"):
            st.write(response)
        messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
