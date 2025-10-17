"""new_table_image

Revision ID: f756149158b9
Revises: 708a82c7a363
Create Date: 2025-10-16 09:12:18.094287

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f756149158b9"
down_revision = "708a82c7a363"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("ext_file", sa.String(), nullable=True),
        sa.Column("url_file", sa.String(), nullable=False),
        sa.Column("size_file", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
    )


def downgrade():
    op.drop_table("images")
