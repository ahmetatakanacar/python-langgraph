from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    age: int
    skills: list[str]
    final: str

def greet_node(state: AgentState) -> dict:
    """First node of our sequence"""
    return {"final": f"Hi {state['name']}!"}

def age_node(state: AgentState) -> dict:
    """Second node of our sequence"""
    return {"final": state["final"] + f" You are {state['age']} years old."}

def skills_node(state: AgentState) -> dict:
    """Third node of our sequence"""
    return {"final": state["final"] + f" You have skills in: {', '.join(state['skills'])}."}

graph = StateGraph(AgentState)
graph.add_node("greet", greet_node)
graph.add_node("add_age", age_node)
graph.add_node("add_skills", skills_node)

graph.add_edge(START, "greet")
graph.add_edge("greet", "add_age")
graph.add_edge("add_age", "add_skills")
graph.add_edge("add_skills", END)

app = graph.compile()

if __name__ == "__main__":
    final_state = app.invoke({
        "name": "Bob",
        "age": 30,
        "skills": ["Python", "Machine Learning", "LangGraph"],
        "final": "",
    })
    print(final_state["final"])