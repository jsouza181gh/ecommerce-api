"""assign roles permissions

Revision ID: b32832ab8c8f
Revises: aecf436312b5
Create Date: 2026-09-26 20:20:17.716383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

revision: str = 'b32832ab8c8f'
down_revision: Union[str, Sequence[str], None] = 'aecf436312b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

role_permissions_table = sa.table(
    "role_permissions",
    sa.column("role_id", sa.UUID),
    sa.column("permission_id", sa.UUID)
)

def get_default_role_permissions():
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.UUID),
        sa.column("name", sa.String)
    )

    permissions_table = sa.table(
        "permissions",
        sa.column("id", sa.UUID),
        sa.column("name", sa.String)
    )

    all_role_permissions = (
        sa.select(
            roles_table.c.id,
            permissions_table.c.id
        )
    )

    admin_permissions = (
        all_role_permissions
        .where(roles_table.c.name == "ADMIN")
    )

    manager_permissions = (
        all_role_permissions
        .where(roles_table.c.name == "MANAGER")
        .where(permissions_table.c.name != "users:create")
    )

    customer_permissions = (
        all_role_permissions
        .where(roles_table.c.name == "CUSTOMER")
        .where(
            permissions_table.c.name.in_([
                "users:read",
                "users:update",
                "users:activate",
                "users:deactivate",
                "auth:signout",
                "auth:refresh"
            ])
        )
    )

    return admin_permissions.union_all(
        manager_permissions,
        customer_permissions
    )


def upgrade() -> None:
    """Upgrade schema."""

    default_role_permissions = get_default_role_permissions()

    insert_all_role_permissions = (
        insert(role_permissions_table)
        .from_select(
            ["role_id", "permission_id"],
            default_role_permissions
        )
    )

    op.execute(insert_all_role_permissions)


def downgrade() -> None:
    """Downgrade schema."""

    default_role_permissions = get_default_role_permissions()

    stmt = (
        role_permissions_table.delete()
        .where(
            sa.tuple_(
                role_permissions_table.c.role_id,
                role_permissions_table.c.permission_id,
            )
            .in_(
                default_role_permissions
            )
        )
    )

    op.execute(stmt)