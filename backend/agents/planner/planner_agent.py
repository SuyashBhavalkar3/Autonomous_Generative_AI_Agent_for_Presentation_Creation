from .schemas import ExecutionPlan, PlanStep
from ..registry import ALLOWED_AGENTS

class PlannerAgent:
    def __init__(self):
        pass

    def create_plan(self, user_goal: str) -> ExecutionPlan:
        """
        Create an execution plan including all relevant agents.
        Sequence: research -> content -> images -> slides -> code (optional)
        """
        if not user_goal or not user_goal.strip():
            raise ValueError("User goal cannot be empty")

        steps = []
        step_id = 1
        goal_lower = user_goal.lower()

        # 1️⃣ Research step (only step with initial input)
        if any(keyword in goal_lower for keyword in ["research", "analyze", "ppt", "presentation"]):
            steps.append(
                PlanStep(
                    step_id=step_id,
                    agent="research_agent",
                    action="Research the topic and gather key points",
                    input=user_goal  # Only step that explicitly gets user goal
                )
            )
            step_id += 1

        # 2️⃣ Content creation (input comes from previous step automatically)
        if any(keyword in goal_lower for keyword in ["ppt", "presentation"]):
            steps.append(
                PlanStep(
                    step_id=step_id,
                    agent="content_agent",
                    action="Create slide-wise structured content"
                )
            )
            step_id += 1

        # 3️⃣ Image collection
        if any(keyword in goal_lower for keyword in ["ppt", "presentation"]):
            steps.append(
                PlanStep(
                    step_id=step_id,
                    agent="image_agent",
                    action="Fetch relevant images for the slides"
                )
            )
            step_id += 1

        # 4️⃣ Slide generation
        if any(keyword in goal_lower for keyword in ["ppt", "presentation"]):
            steps.append(
                PlanStep(
                    step_id=step_id,
                    agent="slide_agent",
                    action="Generate slides using content and images"
                )
            )
            step_id += 1

        # 5️⃣ Optional code agent if goal mentions code/demo
        if any(keyword in goal_lower for keyword in ["code", "demo"]):
            steps.append(
                PlanStep(
                    step_id=step_id,
                    agent="code_agent",
                    action="Generate relevant code snippet"
                )
            )
            step_id += 1

        # Safety fallback: if no steps detected
        if not steps:
            steps.append(
                PlanStep(
                    step_id=1,
                    agent="content_agent",
                    action="Understand the goal and generate relevant output",
                    input=user_goal
                )
            )

        # Normalize step IDs
        for i, step in enumerate(steps, start=1):
            step.step_id = i

        # Validate agents
        invalid_agents = {s.agent for s in steps} - ALLOWED_AGENTS
        if invalid_agents:
            raise ValueError(f"Invalid agents detected: {invalid_agents}")

        return ExecutionPlan(goal=user_goal, steps=steps)