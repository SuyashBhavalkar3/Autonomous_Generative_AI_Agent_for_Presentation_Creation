from typing import Dict, List, Optional, Any
from pydantic import BaseModel

# -------------------------
# Existing (keep for now)
# -------------------------


class PlannerRequest(BaseModel):
    goal: str
    num_slides: Optional[int] = None  # <-- Add this


class PlanStep(BaseModel):
    step_id: int
    agent: str
    action: str
    input: Optional[str] = None


class ExecutionPlan(BaseModel):
    goal: str
    steps: List[PlanStep]


# -------------------------
# New Graph-based Schemas
# -------------------------

class NodeSpec(BaseModel):
    """
    Represents a single graph node (agent).
    Accepts structured input (str, dict, etc.) for LangGraph.
    """
    agent: str
    input: Optional[Any] = None  # <-- Only one field, accepts any type


class GraphSpec(BaseModel):
    """
    Represents a LangGraph-style execution graph.
    """
    goal: str
    nodes: Dict[str, NodeSpec]
    edges: List[tuple[str, str]]
    entry_nodes: List[str]