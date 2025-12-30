from fastapi import APIRouter

from .executor_agent import GraphExecutor
from ..planner.planner_agent import PlannerAgent
from .schemas import ExecutorRequest, ExecutorResponse

router = APIRouter(prefix="/executor", tags=["Executor"])

planner = PlannerAgent()
executor = GraphExecutor()


@router.post("/run", response_model=ExecutorResponse)
async def run_execution(request: ExecutorRequest):
    """
    Execute a LangGraph-style execution graph.
    """
    # 1️⃣ Build graph from planner
    graph = planner.create_plan(request.goal)

    # 2️⃣ Execute graph
    final_state = await executor.execute(graph)

    # 3️⃣ Format response (exclude meta keys like 'goal')
    results = [
        {
            "node": node_id,
            "agent": graph.nodes[node_id].agent,
            "output": output,
        }
        for node_id, output in final_state.items()
        if node_id != "goal"
    ]

    return {"results": results}