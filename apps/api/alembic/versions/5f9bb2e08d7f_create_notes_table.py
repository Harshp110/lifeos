"""create notes table"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "5f9bb2e08d7f"
down_revision = "ecb8cec12a29"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "notes",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
        ),
        sa.Column(
            "title",
            sa.String(200),
            nullable=False,
        ),
        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey(
                "users.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
    )


def downgrade():
    op.drop_table("notes")