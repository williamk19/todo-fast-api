from fastapi import FastAPI
import uvicorn
from src.models import model
from src.database.database import engine
from src.routers import auth, todos, admin, users

app = FastAPI()
model.Base.metadata.create_all(bind=engine)


@app.get("/")
async def test():
    return {"message": "Test Berhasil"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)