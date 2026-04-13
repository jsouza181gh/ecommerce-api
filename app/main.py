import app.config
from fastapi import FastAPI

from infrastructure.database.base import createDataBase
from modules.product.controllers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

@app.get('/', tags=['Health'])
async def health():
    return {'status': 'ok'}

if __name__ == "__main__":
    createDataBase(drop_all=False)