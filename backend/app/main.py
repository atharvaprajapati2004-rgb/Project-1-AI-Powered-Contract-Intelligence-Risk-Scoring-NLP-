from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.analysis import router as analysis_router
from backend.app.routes.document import router as document_router
from backend.app.routes.system import router as system_router
from backend.app.routes.search import router as search_router


app = FastAPI(
    title="AI-Powered Contract Intelligence API",
    description="API for contract clause extraction and risk analysis.",
    version="1.0.0",
)


# Allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(analysis_router)
app.include_router(document_router)
app.include_router(system_router)
app.include_router(search_router)


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