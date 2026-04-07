import os
import sys
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.curdir)
sys.path.insert(0, BASE_DIR)

load_dotenv()

MERCADOPAGO_ACCESS_TOKEN = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY')