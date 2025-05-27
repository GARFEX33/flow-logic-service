"""HTTP interface for the FastAPI application."""

from fastapi import FastAPI
from .main import app

__all__ = ["app"]