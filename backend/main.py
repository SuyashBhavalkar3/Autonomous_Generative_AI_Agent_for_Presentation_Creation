from fastapi import FastAPI
from agents.planner.routes import router as planner_router
from agents.executor.routes import router as executor_router
from agents.planner.planner_agent import PlannerAgent
from agents.executor.executor_agent import GraphExecutor
from fastapi import HTTPException, Request
from pydantic import BaseModel, Field
import os
import uuid



# If you have auth middleware, import it here
# from auth.dependencies import get_current_user

app = FastAPI(
    title="Autonomous PPT Generation API",
    description="LangGraph-style DAG-based autonomous multi-agent system",
    version="1.0.0",
)

# Include routers
app.include_router(planner_router)
app.include_router(executor_router)


class GeneratePPTRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    num_slides: int = Field(5, ge=1, le=14)


@app.post("/generate_ppt")
async def generate_ppt(req: GeneratePPTRequest, request: Request):
    """
    Endpoint that accepts:
      - `prompt` (str): topic/goal for presentation
      - `num_slides` (int): desired number of slides (1-14)

    Returns JSON with `ppt_path` and `slides` metadata (title, bullets, image_url).
    """
    prompt = req.prompt.strip()
    num_slides = int(req.num_slides)

    # Build plan and execute DAG
    planner = PlannerAgent()
    executor = GraphExecutor()

    graph = planner.create_plan(prompt, num_slides=num_slides)

    final_state = await executor.execute(graph)

    # Debug: persist final_state for inspection (temporary)
    import json
    os.makedirs("output", exist_ok=True)
    try:
        with open(os.path.join("output", "debug_state.json"), "w", encoding="utf-8") as f:
            json.dump(final_state, f, default=str, indent=2)
    except Exception:
        pass

    # The executor_agent node should create the PPT and return its path in state['executor_agent']['output_file']
    executor_out = final_state.get("executor_agent") or {}
    output_file = None
    if isinstance(executor_out, dict):
        output_file = executor_out.get("output_file")

    if not output_file or not os.path.exists(output_file):
        # If executor_agent didn't produce a file, return an informative error
        raise HTTPException(status_code=500, detail="Presentation build failed or output file missing")

    # Return the generated PPT file directly as a downloadable response
    from fastapi.responses import FileResponse

    filename = os.path.basename(output_file)
    return FileResponse(output_file, filename=filename)

# Optional: root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Autonomous PPT Generation API"}

# Optional: health check
@app.get("/health")
def health_check():
    return {"status": "ok"}