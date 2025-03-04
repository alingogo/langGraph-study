from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langchain_core.runnables import RunnableConfig
from langgraph.graph.message import add_messages


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: str


graph_builder = StateGraph(State)

def node1(state: State, config: RunnableConfig):
    print("node1")
    # raise ValueError
    10 * (1/0)
    return {"messages": "me"}

def node2(state: State, config: RunnableConfig):
    print("node2")
    return {"messages": "node2"}

graph_builder.add_node("node1", node1)
graph_builder.add_node("node2", node2)
graph_builder.add_edge(START, "node1")
graph_builder.add_edge("node1", "node2")
graph_builder.add_edge("node2", END)

graph = graph_builder.compile()

try:
    graph.invoke({"messages": "you"})
except ZeroDivisionError as e:
    print("---------")
    print(e)