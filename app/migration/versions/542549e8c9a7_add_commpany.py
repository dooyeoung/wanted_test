"""add commpany

Revision ID: 542549e8c9a7
Revises:
Create Date: 2022-09-03 10:59:01.571005

"""
from alembic import op
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy_utc.sqltypes import UtcDateTime
from sqlalchemy_utils.types.uuid import UUIDType


# revision identifiers, used by Alembic.
revision = "542549e8c9a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "company",
        Column("uuid", UUIDType(), nullable=False),
        Column("created_at", UtcDateTime(timezone=True), nullable=False),
        PrimaryKeyConstraint("uuid"),
    )


def downgrade() -> None:
    op.drop_table("company")
