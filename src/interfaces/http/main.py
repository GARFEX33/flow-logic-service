"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/health", response_class=JSONResponse)
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "ok",
            "service": "flow-logic-service",
            "environment": "development"
        }
    )