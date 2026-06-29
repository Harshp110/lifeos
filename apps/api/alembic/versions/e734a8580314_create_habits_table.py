"""create habits table"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "e734a8580314"
down_revision = "5f9bb2e08d7f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "habits",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("completed_today", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("habits")