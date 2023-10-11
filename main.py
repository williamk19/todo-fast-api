from fastapi import FastAPI
import src.models.models as models
from src.database.database import engine
from src.routers import auth, todos

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def test():
    return {"message": "Test Berhasil"}


app.include_router(auth.router)
app.include_router(todos.router)
