from .product_description_image import router as description_image_router
from .product_description_section import router as description_router
from .product_category import router as category_router
from .product_review import router as review_router
from .product_image import router as image_router
from .product import router as product_router

routers = [
    description_image_router,
    description_router,
    category_router,
    review_router,
    product_router,
    image_router
]