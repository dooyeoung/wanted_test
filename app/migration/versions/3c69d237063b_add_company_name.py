"""add company_name

Revision ID: 3c69d237063b
Revises: 542549e8c9a7
Create Date: 2022-09-03 11:19:08.812055

"""
from alembic import op
from sqlalchemy import Column, ForeignKeyConstraint, PrimaryKeyConstraint, String
from sqlalchemy_utils.types.uuid import UUIDType


# revision identifiers, used by Alembic.
revision = "3c69d237063b"
down_revision = "542549e8c9a7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "company_name",
        Column("uuid", UUIDType(), nullable=False),
        Column("company_uuid", UUIDType(), nullable=False),
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
        index_name="ix_company_name",
        table_name="company_name",
        columns=["name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("company_name")
