from fastapi import APIRouter
from .schemas import PlannerRequest, GraphSpec
from .planner_agent import PlannerAgent

router = APIRouter(
    prefix="/planner",
    tags=["Planner"]
)

planner_agent = PlannerAgent()

@router.post(
    "/plan",
    response_model=GraphSpec,
    status_code=200,
    summary="Generate an execution graph from a user goal"
)
def create_execution_graph(request: PlannerRequest):
    """
    Create a LangGraph-style execution graph.
    """
    return planner_agent.create_plan(
        user_goal=request.goal,
        num_slides=request.num_slides  # <-- Pass the user input
    )