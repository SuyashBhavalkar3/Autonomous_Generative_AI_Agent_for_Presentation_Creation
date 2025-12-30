from pydantic import BaseModel
from typing import Any, List


class ExecutorRequest(BaseModel):
    """
    Executor request now only needs the user goal.
    Planner builds the graph internally.
    """
    goal: str


class ExecutorNodeResult(BaseModel):
    """
    Represents the output of a graph node.
    """
    node: str
    agent: str
    output: Any


class ExecutorResponse(BaseModel):
    """
    Graph execution response.
    """
    results: List[ExecutorNodeResult]