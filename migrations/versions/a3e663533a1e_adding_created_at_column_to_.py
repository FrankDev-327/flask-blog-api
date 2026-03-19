"""adding_created_at_column_to_notification_table

Revision ID: a3e663533a1e
Revises: 7bafdf6f5100
Create Date: 2025-09-25 19:54:40.502719

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = "a3e663533a1e"
down_revision = "7bafdf6f5100"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    column_name = "created_at"
    table_name = "notifications"
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    if column_name not in columns:
        op.add_column(
            table_name, sa.Column(column_name, sa.DateTime, default=sa.func.now())
        )


def downgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    column_name = "created_at"
    table_name = "notifications"
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    if column_name not in columns:
        op.drop_column(
            table_name, sa.Column(column_name, sa.DateTime, default=sa.func.now())
        )
