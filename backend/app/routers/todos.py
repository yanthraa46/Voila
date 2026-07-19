from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoDeleteOut, TodoOut, TodoUpdate

# API CONTRACT
# GET /api/todos
#   response: list[{id: int, title: str, completed: bool}]
# POST /api/todos
#   request:  {title: str}
#   response: {id: int, title: str, completed: bool}
# PATCH /api/todos/{id}
#   request:  {completed: bool}
#   response: {id: int, title: str, completed: bool}
# DELETE /api/todos/{id}
#   response: {success: true}

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[TodoOut])
async def list_todos(db: Session = Depends(get_db)) -> list[Todo]:
    try:
        return db.query(Todo).order_by(Todo.created_at.desc()).all()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="failed to load todos") from exc


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
async def create_todo(body: TodoCreate, db: Session = Depends(get_db)) -> Todo:
    try:
        todo = Todo(title=body.title, completed=False)
        db.add(todo)
        db.flush()
        db.refresh(todo)
        return todo
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="failed to create todo") from exc


@router.patch("/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id: str, body: TodoUpdate, db: Session = Depends(get_db)) -> Todo:
    try:
        todo = db.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="todo not found")
        todo.completed = body.completed
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail="failed to update todo") from exc


@router.delete("/{todo_id}", response_model=TodoDeleteOut)
async def delete_todo(todo_id: str, db: Session = Depends(get_db)) -> TodoDeleteOut:
    try:
        todo = db.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="todo not found")
        db.delete(todo)
        db.flush()
        return TodoDeleteOut(success=True)
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="failed to delete todo") from exc
