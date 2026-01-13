from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.planner.routes import router as planner_router
from agents.executor.routes import router as executor_router
from auth.routes import router as auth_router
from agents.planner.planner_agent import PlannerAgent
from agents.executor.executor_agent import GraphExecutor
from fastapi import HTTPException, Request
from pydantic import BaseModel, Field
import os
import uuid
from auth.dependencies import get_current_user
from fastapi import Depends


# If you have auth middleware, import it here
# from auth.dependencies import get_current_user

app = FastAPI(
    title="Autonomous PPT Generation API",
    description="LangGraph-style DAG-based autonomous multi-agent system",
    version="1.0.0",
)

# Allow frontend dev server to talk to backend
# Configure CORS. In production set `ALLOWED_ORIGINS` to a comma-separated
# list of origins (eg. https://app.example.com). For local development the
# common Vite origins are included by default.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length"],
)

# Include routers
app.include_router(auth_router)
app.include_router(planner_router, dependencies=[Depends(get_current_user)])
app.include_router(executor_router, dependencies=[Depends(get_current_user)])


class GeneratePPTRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    num_slides: int = Field(5, ge=1, le=14)


@app.post("/generate_ppt", dependencies=[Depends(get_current_user)])
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
        # If executor_agent didn't produce a file, attempt to build here using slides
        # Reuse existing ppt_builder which supports downloading images from `image_url`.
        try:
            from ppt.ppt_builder import build_presentation
            from pathlib import Path

            # Prefer slides produced by executor_agent if present, else fallback to slide_agent
            slides = None
            if isinstance(executor_out, dict):
                slides = executor_out.get("slides")
            if not slides:
                slide_agent_out = final_state.get("slide_agent") or {}
                if isinstance(slide_agent_out, dict):
                    slides = slide_agent_out.get("slides")

            if not slides:
                raise HTTPException(status_code=500, detail="Presentation build failed or output file missing")

            out_dir = Path("output") / "presentations"
            out_dir.mkdir(parents=True, exist_ok=True)
            import uuid as _u
            filename = f"presentation_fallback_{_u.uuid4().hex}.pptx"
            out_path = out_dir / filename

            # build_presentation will download images when slides include `image_url`
            build_presentation(slides, out_path)
            output_file = str(out_path)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Presentation build failed: {e}")

    # Return the generated PPT file directly as a downloadable response
    from fastapi.responses import FileResponse

    # Explicitly set media type for PPTX and ensure a UTF-8 encoded
    # `Content-Disposition` header so browsers save the file correctly.
    from urllib.parse import quote

    filename = os.path.basename(output_file)
    quoted = quote(filename)
    headers = {
        "Content-Disposition": f"attachment; filename*=UTF-8''{quoted}"
    }

    return FileResponse(
        output_file,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers=headers,
    )

# Optional: root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Autonomous PPT Generation API"}

# Optional: health check
@app.get("/health")
def health_check():
    return {"status": "ok"}