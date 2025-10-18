"""added_new_column_into_images

Revision ID: 7de316325f0d
Revises: f756149158b9
Create Date: 2025-10-18 22:15:28.607482

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = "7de316325f0d"
down_revision = "f756149158b9"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    table_name = "images"
    column_name = "public_id"
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    if column_name not in columns:
        op.add_column(table_name, sa.Column(column_name, sa.String(255)))


def downgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    table_name = "users"
    column_name = "password"
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    if column_name in columns:
        op.drop_column(table_name, column_name)
