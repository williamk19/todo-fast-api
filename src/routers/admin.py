from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from ..database.database import SessionLocal
from ..models.model import Todos
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos_admin(user: user_deps, db: db_deps):
    if user is not None and user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorize request"
        )

    todos = db.query(Todos).all()
    return todos


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_admin(user: user_deps, db: db_deps, todo_id: int = Path(gt=0)):
    if user is None and user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorize request"
        )

    query_todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if query_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
