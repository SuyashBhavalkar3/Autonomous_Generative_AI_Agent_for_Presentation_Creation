from fastapi import APIRouter
from .executor_agent import ExecutorAgent
from .schemas import ExecutorRequest, ExecutorResponse

router = APIRouter(prefix="/executor", tags=["Executor"])
executor_agent = ExecutorAgent()

@router.post("/run", response_model=ExecutorResponse)
async def run_execution_plan(request: ExecutorRequest):
    # Convert request to internal plan
    plan = executor_agent.parse_request(request)
    
    # Await execution
    results_dict = await executor_agent.execute_plan(plan)
    
    # Return as ExecutorResponse
    results = [
        {"step_id": sid, "agent": step.agent if (step := plan.steps[i-1]) else "unknown", "output": out}
        for i, (sid, out) in enumerate(results_dict.items(), start=1)
    ]
    
    return {"results": results}