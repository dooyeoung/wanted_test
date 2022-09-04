"""add company_tag

Revision ID: fd9c851742b2
Revises: 3c69d237063b
Create Date: 2022-09-03 11:19:12.098119

"""
from alembic import op
from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    Integer,
)
from sqlalchemy_utils.types.uuid import UUIDType


# revision identifiers, used by Alembic.
revision = "fd9c851742b2"
down_revision = "3c69d237063b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "company_tag",
        Column("uuid", UUIDType(), nullable=False),
        Column("company_uuid", UUIDType(), nullable=False),
        Column("group_id", Integer(), nullable=False),
        Column("name", String(length=20), nullable=False),
        Column("language", String(length=2), nullable=False),
        ForeignKeyConstraint(
            columns=["company_uuid"],
            refcolumns=["company.uuid"],
            ondelete="cascade",
        ),
        PrimaryKeyConstraint("uuid"),
    )
    op.create_index(
        index_name="ix_company_tag",
        table_name="company_tag",
        columns=["name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("company_tag")
