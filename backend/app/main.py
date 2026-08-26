from fastapi import FastAPI

from backend.app.routes.analysis import router as analysis_router


app = FastAPI(
    title="AI-Powered Contract Intelligence API",
    description="API for contract clause extraction and risk analysis.",
    version="1.0.0",
)


app.include_router(analysis_router)


@app.get("/")
def root():
    return {
        "message": "AI-Powered Contract Intelligence API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }