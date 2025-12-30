from fastapi import FastAPI
from agents.planner.routes import router as planner_router
from agents.executor.routes import router as executor_router

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

# Optional: root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Autonomous PPT Generation API"}

# Optional: health check
@app.get("/health")
def health_check():
    return {"status": "ok"}