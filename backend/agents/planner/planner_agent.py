from ..registry import ALLOWED_AGENTS
from .schemas import GraphSpec, NodeSpec


class PlannerAgent:
    """
    LangGraph-style planner agent that generates a DAG of nodes for execution.
    """

    def __init__(self):
        pass

    def create_plan(self, user_goal: str, num_slides: int = None) -> GraphSpec:
        if not user_goal or not user_goal.strip():
            raise ValueError("User goal cannot be empty")

        # Convert to int if provided
        if num_slides is not None:
            num_slides = int(num_slides)

        # Default to 14 if not provided
        if num_slides is None:
            num_slides = 14

        # Clamp to 1–14
        num_slides = max(1, min(num_slides, 14))

        # Build nodes
        # Do not inject num_slides via NodeSpec.input; use shared GraphSpec/state
        nodes = {
            "research_agent": NodeSpec(agent="research_agent", input=user_goal),
            "content_agent": NodeSpec(agent="content_agent", input=None),
            "image_agent": NodeSpec(agent="image_agent", input=None),
            "slide_agent": NodeSpec(agent="slide_agent", input=None),
        }

        edges = [
            ("research_agent", "content_agent"),
            ("content_agent", "image_agent"),
            ("content_agent", "slide_agent"),
        ]

        entry_nodes = ["research_agent"]

        # Validate agents
        invalid_agents = {node.agent for node in nodes.values()} - ALLOWED_AGENTS
        if invalid_agents:
            raise ValueError(f"Invalid agents detected: {invalid_agents}")

        return GraphSpec(goal=user_goal, nodes=nodes, edges=edges, entry_nodes=entry_nodes, num_slides=num_slides)
