"""add default permissions

Revision ID: aecf436312b5
Revises: 3733d1fbe055
Create Date: 2026-09-26 12:09:17.733298

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

revision: str = 'aecf436312b5'
down_revision: Union[str, Sequence[str], None] = '3733d1fbe055'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

public_resources = [
    "categories",
    "description_images",
    "description_sections",
    "product_images",
    "review_images",
    "product_reviews",
    "products",
]

base_permission_types = [
    "create",
    "read",
    "list",
    "update",
    "delete"
]

user_permission_types = [
    *base_permission_types,
    "activate",
    "deactivate"
]

auth_permission_types = [
    "signout",
    "refresh"
]

def get_initial_permissions() -> list[str]:
    public_permissions = [
        f"{resource}:{permission}"
        for resource in public_resources
        for permission in base_permission_types
    ]

    user_permissions = [
        f"users:{permission}"
        for permission in user_permission_types
    ]

    auth_permissions = [
        f"auth:{permission}"
        for permission in auth_permission_types
    ]

    return public_permissions + user_permissions + auth_permissions


permissions_table = sa.table(
    "permissions",
    sa.column("name", sa.String),
)

def upgrade() -> None:
    """Upgrade schema."""

    initial_permissions = get_initial_permissions()

    stmt = (
        insert(permissions_table)
        .values(
            [
                {"name": permission}
                for permission in initial_permissions
            ]
        )
        .on_conflict_do_nothing(
            index_elements=["name"]
        )
    )

    op.execute(stmt)


def downgrade()-> None:
    """Downgrade schema."""
    
    initial_permissions = get_initial_permissions()
    
    stmt = (
        permissions_table.delete()
        .where(
            permissions_table.c.name.in_(initial_permissions)
        )
    )

    op.execute(stmt)
    