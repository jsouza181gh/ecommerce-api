import os
from dotenv import load_dotenv

load_dotenv()

required = [
    "DATABASE_HOST", 
    "DATABASE_NAME", 
    "DATABASE_USER", 
    "DATABASE_PASSWORD", 
    "DEFAULT_CURRENCY", 
    "JWT_SECRET_KEY", 
    "JWT_ALGORITHM", 
    "JWT_EXPIRE_MINUTES",
    "REFRESH_TOKEN_EXPIRE_DAYS"
    "DEFAULT_ROLE"
]

missing = [key for key in required if not os.getenv(key)]

if missing:
    raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

DATABASE_URL = fr"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

JWT_SECRET_KEY = str(os.getenv("JWT_SECRET_KEY"))
JWT_ALGORITHM = str(os.getenv("JWT_ALGORITHM"))
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY')
DEFAULT_ROLE= str(os.getenv("DEFAULT_ROLE"))

MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')