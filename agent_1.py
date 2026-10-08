from typing import Dict, TypedDict, Any
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message : str

def greeting_node(state: AgentState) -> AgentState:
    """
    Simple greeting node that returns a greeting message based on the input state.
    """
    state["message"] = "Hello! How can I assist you today?"
    return state

graph = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    initial_state: AgentState = {"message": ""}
    final_state: AgentState = app.invoke(initial_state)
    print(final_state["message"])