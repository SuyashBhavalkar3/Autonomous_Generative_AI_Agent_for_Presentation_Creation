from pydantic import BaseModel
from typing import List, Optional

class ExecutorStepResult(BaseModel):
    step_id: int
    agent: str
    output: Optional[str]

class ExecutorRequest(BaseModel):
    goal: str
    steps: List[dict]  # Accepts Planner ExecutionPlan JSON

class ExecutorResponse(BaseModel):
    results: List[ExecutorStepResult]