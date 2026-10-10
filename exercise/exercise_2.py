from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    number3: int
    number4: int
    operation1: str
    operation2: str
    finalNumber1: int
    finalNumber2: int

def adder_operation1(state: AgentState) -> dict:
    """This node adds the two numbers"""

    state["finalNumber1"] = state["number1"] + state["number2"]
    return state 

def subtractor_operation1(state: AgentState) -> dict:
    """This node subtracts the two numbers"""

    state["finalNumber1"] = state["number1"] - state["number2"]
    return state

def adder_operation2(state: AgentState) -> dict:
    """This node adds the two numbers"""
    
    state["finalNumber2"] = state["number3"] + state["number4"]
    return state

def substractor_operation2(state: AgentState) -> dict:
    """"This node subtracts the two numbers"""

    state["finalNumber2"] = state["number3"] - state["number4"]
    return state

def decide_next_node_operation1(state: AgentState) -> str:
    """This node will select the next node of the graph"""

    if state["operation1"] == "+":
        return "addition_operation1"

    elif state["operation1"] == "-":
        return "subtraction_operation1"

def decide_next_node_operation2(state: AgentState) -> str:
    """This node will select the next node of the graph"""

    if state["operation2"] == "+":
        return "addition_operation2"

    elif state["operation2"] == "-":
        return "subtraction_operation2"

graph = StateGraph(AgentState)

graph.add_node("add_node1", adder_operation1)
graph.add_node("subtract_node1", subtractor_operation1)
graph.add_node("router1", lambda state:state) 
graph.add_node("add_node2", adder_operation2)
graph.add_node("subtract_node2", substractor_operation2)    
graph.add_node("router2", lambda state:state) 

graph.add_edge(START, "router1")
graph.add_conditional_edges(
    "router1",
    decide_next_node_operation1,
    {
        "addition_operation1": "add_node1",
        "subtraction_operation1": "subtract_node1"
    }
)
graph.add_edge("add_node1", "router2")
graph.add_edge("subtract_node1", "router2")
graph.add_conditional_edges(
    "router2",
    decide_next_node_operation2,
    {
        "addition_operation2": "add_node2",
        "subtraction_operation2": "subtract_node2"
    }
)
graph.add_edge("add_node2", END)
graph.add_edge("subtract_node2", END)

app = graph.compile()

if __name__ == "__main__":
    initial_state = AgentState(number1=10, operation1="-", number2=5, number3=20, operation2="+", number4=10)
    final_state = app.invoke(initial_state)
    print(final_state)