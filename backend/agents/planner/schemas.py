from typing import List, Optional
from pydantic import BaseModel


class PlannerRequest(BaseModel):
    goal: str


class PlanStep(BaseModel):
    step_id: int
    agent: str
    action: str
    input: Optional[str] = None


class ExecutionPlan(BaseModel):
    goal: str
    steps: List[PlanStep]
