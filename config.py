import os
from dotenv import load_dotenv

load_dotenv()

required = ["DATABASE_HOST", "DATABASE_NAME", "DATABASE_USER", "DATABASE_PASSWORD", "DEFAULT_CURRENCY"]
missing = [key for key in required if not os.getenv(key)]

if missing:
    raise RuntimeError(f"Missing env vars: {', '.join(missing)}")

DATABASE = {
    'HOST' : os.getenv('DATABASE_HOST'),
    'NAME' : os.getenv('DATABASE_NAME'),
    'USER' : os.getenv('DATABASE_USER'),
    'PASSWORD' : os.getenv('DATABASE_PASSWORD')
}

DATABASE_URL = f"postgresql+asyncpg://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['NAME']}"
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY')
ENVIRONMENT = os.getenv('ENVIRONMENT')