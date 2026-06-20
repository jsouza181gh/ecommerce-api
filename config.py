import os
from dotenv import load_dotenv

load_dotenv()

required = ["DATABASE_HOST", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD", "DEFAULT_CURRENCY"]
missing = [key for key in required if not os.getenv(key)]

if missing:
    raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

DATABASE_URL = fr"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY')