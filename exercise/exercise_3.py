from langgraph.graph import StateGraph, END
from typing import List, TypedDict
import random

class AgentState(TypedDict):
    player_name: str
    target_number: int
    guesses: List[int]
    attempts: int
    hint: str
    lower_bound: int
    upper_bound: int

def greeting_node(state: AgentState):
    """Greeting node which says hi to the player"""

    state["player_name"] = f"Hello, {state['player_name']}! Welcome to the Number Guessing Game."
    state["attempts"] = 0
    state["guesses"] = []
    return state

def setup_node(state: AgentState):
    """Setup node which initializes the target number and bounds"""

    state["target_number"] = random.randint(1, 20)
    state["lower_bound"] = 1
    state["upper_bound"] = 20
    state["hint"] = "Guess a number between 1 and 20."
    return state

def guess_node(state: AgentState):
    """Node where the player makes a guess"""

    guess = random.randint(state["lower_bound"], state["upper_bound"])
    state["guesses"].append(guess)
    state["attempts"] += 1

    if guess < state["target_number"]:
        state["hint"] = f"Your guess of {guess} is too low. Try again."
        state["lower_bound"] = guess + 1
    elif guess > state["target_number"]:
        state["hint"] = f"Your guess of {guess} is too high. Try again."
        state["upper_bound"] = guess - 1
    else:
        state["hint"] = f"Congratulations! You've guessed the number {state['target_number']} in {state['attempts']} attempts."

    return state

def should_continue(state: AgentState) -> str:
    """Function to decide what to do next"""

    if state["guesses"][-1] == state["target_number"] or state["attempts"] >= 7:
        return "exit"
    else:
        print("ENTERING LOOP", state["attempts"])
        return "loop"

graph = StateGraph(AgentState)
graph.add_node("greeting", greeting_node)
graph.add_node("setup", setup_node)
graph.add_node("guess", guess_node)

graph.set_entry_point("greeting")
graph.add_edge("greeting", "setup")
graph.add_edge("setup", "guess")

graph.add_conditional_edges(
    "guess",
    should_continue,
    {
        "loop": "guess",
        "exit": END
    }
)

app = graph.compile()

if __name__ == "__main__":
    initial_state: AgentState = {
        "player_name": "Student",
        "target_number": 0,
        "guesses": [],
        "attempts": 0,
        "hint": "",
        "lower_bound": 1,
        "upper_bound": 20
    }
    final_state = app.invoke(initial_state)
    print(final_state["player_name"])
    print(final_state["guesses"])
    print(final_state["hint"])