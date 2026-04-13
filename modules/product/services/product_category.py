from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from uuid import UUID

from ..schemas import SaveProductCategorySchema, ProductCategorySchema
from ..repositories import ProductCategoryRepository
from ..models import ProductCategory

@dataclass
class ProductCategoryService:
    category_repository: ProductCategoryRepository

    async def create(self, category_schema: SaveProductCategorySchema) -> ProductCategorySchema:
        category = ProductCategory(
            name=category_schema.name
        )

        try:
            new_category = await self.category_repository.create(category)

        except IntegrityError:
            await self.category_repository.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category already exists'
            )

        return ProductCategorySchema(
            id=new_category.id,
            name=new_category.name
        )
    

    async def get(self, category_id: UUID) -> ProductCategorySchema:
        category = await self.category_repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        return ProductCategorySchema(
            id= category.id,
            name=category.name
        )
    

    async def list(self, name: Optional[str]) -> List[ProductCategorySchema]:
        categories = await self.category_repository.list(name)

        categories = [
            ProductCategorySchema(
                id=category.id,
                name=category.name
            )
            for category in categories
        ]

        return categories
    

    async def update(
        self,
        category_id: UUID,
        category_schema: SaveProductCategorySchema
    ) -> ProductCategorySchema:

        category = await self.category_repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        category.name = category_schema.name

        try:
            new_category = await self.category_repository.update(category)

        except IntegrityError:
            await self.category_repository.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category with this name already exists'
            )

        return ProductCategorySchema(
            id=new_category.id,
            name=new_category.name
        )
    
    async def delete(self, category_id: UUID) -> None:
        category = await self.category_repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        await self.category_repository.delete(category)