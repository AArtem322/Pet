from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers.books import router as books_router
from app.api.routers.categories import router as categories_router
from app.db.session import engine
from app.models.base import Base





app = FastAPI()
app.include_router(books_router)
app.include_router(categories_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)
