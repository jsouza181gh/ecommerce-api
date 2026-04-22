import os
import sys
import asyncio
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, BASE_DIR)

load_dotenv()

MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY')
ENVIRONMENT = os.getenv('ENVIRONMENT')


if __name__ == "__main__" and ENVIRONMENT == 'development':
    from infrastructure.database.base import createDataBase
    asyncio.run(createDataBase(drop_all=False))