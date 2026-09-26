"""make description nullable in Product Review

Revision ID: 371cf63ee632
Revises: 17ee7b27044d
Create Date: 2026-06-08 18:55:15.758779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '371cf63ee632'
down_revision: Union[str, Sequence[str], None] = '17ee7b27044d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column('product_reviews', 'description',
               existing_type=sa.TEXT(),
               nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    
    op.alter_column('product_reviews', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
