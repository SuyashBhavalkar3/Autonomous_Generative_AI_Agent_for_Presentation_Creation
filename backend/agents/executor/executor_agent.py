# executor_agent.py
from .research_agent import research_agent
from .content_agent import content_agent
from .image_agent import image_agent
from .slide_agent import slide_agent

from ..planner.schemas import ExecutionPlan, PlanStep

AGENT_FUNCTIONS = {
    "research_agent": research_agent,
    "content_agent": content_agent,
    "image_agent": image_agent,
    "slide_agent": slide_agent,
}


class ExecutorAgent:
    """Modular executor that runs plan steps using the goal from ExecutionPlan."""

    def __init__(self):
        self.context = {}  # Store outputs of previous steps keyed by step id

    async def execute_plan(self, plan: ExecutionPlan) -> dict:
        """Execute the given plan sequentially using plan.goal.

        Returns a mapping {step_id: result}.
        """
        results = {}
        for step in plan.steps:
            result = await self._execute_step(step, plan.goal)
            results[step.step_id] = result
            self.context[f"step_{step.step_id}"] = result
        return results

    async def _execute_step(self, step: PlanStep, goal: str):
        if step.agent not in AGENT_FUNCTIONS:
            raise NotImplementedError(f"Agent {step.agent} not implemented")

        # Build structured input for the agent
        if step.input is None:
            input_payload = {
                "goal": goal,
                "previous_output": self._get_previous_output(),
                "action": step.action,
            }
        else:
            # If explicit input provided, unify into dict form if necessary
            input_payload = step.input if isinstance(step.input, dict) else {"text": step.input}

        agent_fn = AGENT_FUNCTIONS[step.agent]
        return await agent_fn(input_payload)

    def _get_previous_output(self):
        """Return the output of the last executed step, if any."""
        if not self.context:
            return None
        return list(self.context.values())[-1]

    def parse_request(self, request):
        """Convert ExecutorRequest into ExecutionPlan."""
        steps = [
            PlanStep(
                step_id=step_item.get("step_id"),
                agent=step_item.get("agent"),
                action=step_item.get("action"),
                input=step_item.get("input"),
            )
            for step_item in request.steps
        ]
        return ExecutionPlan(goal=request.goal, steps=steps)