from .product_description_section import router as description_router
from .product_category import router as category_router
from .product_image import router as image_router
from .product import router as product_router

routers = [
    description_router,
    category_router,
    product_router,
    image_router
]