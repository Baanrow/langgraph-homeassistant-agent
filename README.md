# langgraph-homeassistant-agent

Modular GPT agent built with [LangGraph](https://github.com/langchain-ai/langgraph) to control Home Assistant using tool calls and persistent SQLite memory.

This project demonstrates a structured, node-based GPT agent workflow that includes tool invocation, memory persistence, and basic control logic. It’s designed to be extendable and production-ready for automating smart home tasks or integrating with other systems via API.

---

## 🧠 What It Does

- Uses LangGraph to orchestrate a node-based conversational agent
- Calls a Home Assistant API tool to retrieve light state via REST
- Stores state and conversation history in a local SQLite database
- Exposes a chat UI via Streamlit for easy testing

---

## 🗂️ File Structure

| File              | Purpose |
|-------------------|---------|
| `app.py`          | Streamlit UI for interacting with the agent |
| `simple_chain.py` | Wraps the LangGraph graph and manages state/session handling |
| `simple_agent.py` | Defines the LangGraph graph nodes, edges, and tool flow logic |
| `ha_tools.py`     | Tool function for calling Home Assistant to retrieve light state |

---

## 🔧 Tools & Technologies

- **LangGraph** for stateful, tool-enabled graph workflows
- **OpenAI Assistants API** for GPT-based responses
- **Home Assistant API** for smart device control
- **SQLite3** for persistent memory storage
- **Streamlit** for frontend testing interface
- **LangChain ToolNode** for tool handling logic

---

## 🚀 Example Use Case

Ask the agent:  
> "Is the kitchen light on?"  

The agent:
1. Parses the request
2. Decides to call the `get_light_state` tool
3. Calls the Home Assistant API
4. Returns the light status via GPT in a conversational format
5. Logs the conversation in memory

---

## 📦 Notes

- This project is intended as a **demo** and reference architecture.
- To run it locally, you would need your own `.env` file with `HA_TOKEN` and `HA_URL_LOCAL`.
- All logic is modular and can be extended with more tools, FastAPI integration, or memory layers.

---

## 👨‍💻 About

Built by Brett C.  
I specialize in Python-based GPT agents, automation tools, and API workflows.  
This project reflects my focus on building real-world, memory-enabled agent architectures using modern frameworks like LangGraph.
