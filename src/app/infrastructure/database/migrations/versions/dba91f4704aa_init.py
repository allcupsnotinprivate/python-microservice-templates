"""init

Revision ID: dba91f4704aa
Revises:
Create Date: 2025-05-31 11:43:18.925685

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "dba91f4704aa"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "messages",
        sa.Column("author", sa.VARCHAR(length=39), nullable=False),
        sa.Column("content", sa.VARCHAR(length=512), nullable=False),
        sa.Column("reply_to", sa.BIGINT(), nullable=True),
        sa.Column("conversation_id", sa.BIGINT(), nullable=False),
        sa.Column("id", sa.BIGINT(), autoincrement=True, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["reply_to"],
            ["messages.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("conversations")
