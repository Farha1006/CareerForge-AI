"""
CareerForge AI - FastAPI REST API Application Server
Script: backend/app/main.py
Description: Main entrypoint for the CareerForge AI backend REST API.
             Configures CORS middleware, loads routers, and exposes OpenAPI docs.
"""

import os
import sys

# Resolve paths to project root, ml, and deep_learning
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(script_dir, ".."))
project_root = os.path.abspath(os.path.join(backend_dir, ".."))

sys.path.append(backend_dir)
sys.path.append(os.path.join(project_root, "ml"))
sys.path.append(os.path.join(project_root, "deep_learning"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routes import health, student, skill_gap, recommend, predict, market

app = FastAPI(
    title="CareerForge AI - REST API",
    description="An Intelligent Career Intelligence Platform Using Data Engineering, Data Mining and Deep Learning.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware for React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, including http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router)
app.include_router(student.router)
app.include_router(skill_gap.router)
app.include_router(recommend.router)
app.include_router(predict.router)
app.include_router(market.router)


@app.get("/", include_in_schema=False)
def root_redirect():
    """Redirect root path to interactive Swagger API documentation."""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
