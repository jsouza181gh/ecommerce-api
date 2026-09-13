from fastapi import FastAPI

from modules.product.controllers import product_routers
from modules.auth.controllers import auth_routers

app = FastAPI()

for router in [*product_routers, *auth_routers]:
    app.include_router(router)

@app.get('/', tags=['Health'])
async def health():
    return {'status': 'ok'}