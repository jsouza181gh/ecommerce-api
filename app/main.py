from fastapi import FastAPI

import app.config
from modules.product.controllers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

@app.get('/', tags=['Health'])
async def health():
    return {'status': 'ok'}