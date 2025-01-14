from starlette.config import Config

config = Config(".env")
JWT_SECRET = config("JWT_SECRET", default="secret-key")
JWT_ALGO = config("JWT_ALGO", default="HS256")
JWT_EXPIRE = config("JWT_EXPIRE", default=200000)

DB_URL = config("DB_URL", default="postgresql://root:root@localhost:5432/todo_db")
DB_MS = config("DB_MS", default="postgresql")
DB_PORT = config("DB_PORT", default="5432")
DB_NAME = config("DB_NAME", default="todo_db")
DB_USERNAME = config("DB_USERNAME", default="root")
DB_PASSWORD = config("DB_PASSWORD", default="root")
DB_HOST = config("DB_HOST", default="localhost")