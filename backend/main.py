from fastapi import FastAPI

from core.config import JWT_SECRET_KEY

from utils.database import Base, engine

from auth.routes import router as auth_router

app = FastAPI(
    title="Autonomous Generative AI Agent",
    version="1.0.0"
)

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "ok"}