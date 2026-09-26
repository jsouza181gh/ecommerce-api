"""add default roles

Revision ID: 3733d1fbe055
Revises: aae5ff537cf7
Create Date: 2026-09-26 11:25:55.441600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

revision: str = '3733d1fbe055'
down_revision: Union[str, Sequence[str], None]  = 'aae5ff537cf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

default_roles = ["ADMIN", "MANAGER", "CUSTOMER"]

roles_table = sa.table(
    "roles",
    sa.column("name", sa.String),
)

def upgrade() -> None:
    """Upgrade schema."""

    stmt = (
        insert(roles_table)
        .values(
            [
                {"name": role} 
                for role in default_roles
            ]
        )
        .on_conflict_do_nothing(
            index_elements=["name"]
        )
    )

    op.execute(stmt)


def downgrade() -> None:
    """Downgrade schema."""

    stmt = (
        roles_table.delete()
        .where(
            roles_table.c.name.in_(default_roles)
        )
    )

    op.execute(stmt)
