from dataclasses import dataclass

from ..repositories import ProductImageRepository, ProductRepository

@dataclass
class ProductImageService:
    image_repository: ProductImageRepository
    product_repository: ProductRepository

    async def create():
        pass


    async def find_by_id():
        pass


    async def find_all():
        pass


    async def update():
        pass


    async def delete():
        pass