from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""

    state["result"] = f"Hi there {state["name"]}! Your sum = {sum(state["values"])}"
    return state

graph = StateGraph(AgentState)
graph.add_node("processor", process_values)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

if __name__ == "__main__":
    initial_state: AgentState = {"values": [1, 2, 3], "name": "Alice", "result": ""}
    final_state: AgentState = app.invoke(initial_state)
    print(final_state["result"])