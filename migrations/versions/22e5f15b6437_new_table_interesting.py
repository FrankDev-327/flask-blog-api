"""new_table_interesting

Revision ID: 22e5f15b6437
Revises: 8444ea0ea822
Create Date: 2025-10-09 20:58:44.433926

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "22e5f15b6437"
down_revision = "8444ea0ea822"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "interesting",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("interest_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        if_not_exists=True,
    )


def downgrade():
    op.drop_table("interesting")
