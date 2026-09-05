from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.cors import CORSMiddleware

from app.api.routers.books import router as books_router
from app.api.routers.categories import router as categories_router

app = FastAPI()
app.include_router(books_router)
app.include_router(categories_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

counter = 0


@app.middleware("http")
async def request_counter(request: Request, call_next: Callable) -> Response:
    global counter
    counter += 1
    response = await call_next(request)
    response.headers["X-Request-Number"] = str(counter)
    return response
