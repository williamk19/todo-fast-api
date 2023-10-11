from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from starlette import status
from src.database.database import SessionLocal
from sqlalchemy.orm import Session
from src.models.models import Todos
from .auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=10)
    priority: int = Field(ge=1, le=5)
    complete: bool = Field(default=False)


@router.get("/")
async def get_all_todos(user: user_deps, db: db_deps):
    if not (user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorize request"
        )

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_deps, db: db_deps, todo_id: int = Path(gt=0)):
    if not (user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorize request"
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )
    if todo_model is not None:
        return todo_model
    else:
        return HTTPException(status_code=404, detail="Todo not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_deps, db: db_deps, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorize request")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_deps, db: db_deps, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    if not (user):
        raise HTTPException(status_code=401, detail="Unauthorize request")

    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"))
        .filter(Todos.id == todo_id)
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_deps, db: db_deps, todo_id: int = Path(gt=0)):
    if not (user):
        raise HTTPException(status_code=401, detail="Unauthorize request")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
