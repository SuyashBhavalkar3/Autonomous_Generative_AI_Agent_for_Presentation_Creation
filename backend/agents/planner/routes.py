from fastapi import APIRouter, Depends
from .schemas import PlannerRequest, ExecutionPlan
from .planner_agent import PlannerAgent

router = APIRouter(
    prefix="/planner",
    tags=["Planner"]
)

planner_agent = PlannerAgent()


@router.post(
    "/plan",
    response_model=ExecutionPlan,
    status_code=200,
    summary="Generate an execution plan from a user goal"
)
def create_execution_plan(
    request: PlannerRequest,
):
    return planner_agent.create_plan(request.goal)