from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..database.database import SessionLocal
from ..models.model import Users
from .auth import get_current_user


router = APIRouter(prefix="/users", tags=["users"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


@router.get("/user", status_code=status.HTTP_200_OK)
async def get_current_user(user: user_deps, db: db_deps):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorize Request")

    current_user = db.query(Users).filter(Users.id == int(user.get("id"))).first()

    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return current_user


class PasswordRequest(BaseModel):
    current_password: str = Field(min_length=8)
    password: str = Field(min_length=8)


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_password(
    user: user_deps, db: db_deps, password_request: PasswordRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorize Request")

    current_user = db.query(Users).filter(Users.id == user.get("id")).first()
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )

    if not bcrypt_context.verify(
        password_request.current_password, current_user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Unauthorize Request")

    current_user.hashed_password = bcrypt_context.hash(password_request.password)
    db.add(current_user)
    db.commit()


class PhoneRequest(BaseModel):
    phone_number: str = Field(min_length=8, max_length=15)


@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_deps, db: db_deps, phone_request: PhoneRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorize Request")

    current_user = db.query(Users).filter(Users.id == user.get("id")).first()

    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current_user.phone_number = phone_request.phone_number
    db.add(current_user)
    db.commit()
