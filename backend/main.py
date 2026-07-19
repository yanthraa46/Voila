from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import todos

# API CONTRACT
# GET /api/todos
#   response: list[{id: int, title: str, completed: bool}]
# POST /api/todos
#   request:  {title: str}
#   response: {id: int, title: str, completed: bool}
# PATCH /api/todos/{id}
#   request:  {completed: bool}
#   response: {todo: {id: int, title: str, completed: bool}}
# DELETE /api/todos/{id}
#   response: {success: true}
# GET /health
#   response: {ok: true}


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Todo API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(todos.router)


@app.get("/health")
def health() -> dict[str, bool]:
    return {"ok": True}
