from starlette.config import Config

config = Config(".env")
JWT_SECRET = config("JWT_SECRET", default='secret-key')
JWT_ALGO = config("JWT_ALGO", default='HS256')
JWT_EXPIRE = config("JWT_EXPIRE", default=200000)
