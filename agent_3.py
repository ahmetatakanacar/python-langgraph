from typing import TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str
    age: str
    final: str

def first_node(state: AgentState) -> AgentState:
    """This is the first node of our sequence"""

    state["final"] = f"Hi {state['name']}!"
    return state

def second_node(state: AgentState) -> AgentState:
    """This is the second node of our sequence"""

    state["final"] += f" You are {state['age']} years old."
    return state

graph = StateGraph(AgentState)
graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.set_finish_point("second_node")

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    initial_state: AgentState = {"name": "Bob", "age": "30", "final": ""}
    final_state: AgentState = app.invoke(initial_state)
    print(final_state["final"])