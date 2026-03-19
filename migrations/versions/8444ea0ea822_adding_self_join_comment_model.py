"""adding_self_join_comment_model

Revision ID: 8444ea0ea822
Revises: a3e663533a1e
Create Date: 2025-09-25 22:14:13.692732

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = "8444ea0ea822"
down_revision = "a3e663533a1e"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    table_name = "comments"
    column_name = "parent_id"

    columns = [col["name"] for col in inspector.get_columns(table_name)]
    if column_name not in columns:
        op.add_column(table_name, sa.Column(column_name, sa.Integer, nullable=True))
        op.create_foreign_key(
            constraint_name=f"fk_{table_name}_{column_name}",
            source_table=table_name,
            referent_table=table_name,
            local_cols=[column_name],
            remote_cols=["id"],
        )
        op.alter_column(
            table_name, column_name, nullable=False, existing_type=sa.Integer
        )


def downgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)

    table_name = "comments"
    column_name = "parent_id"

    columns = [col["name"] for col in inspector.get_columns(table_name)]
    if column_name not in columns:
        op.drop_constraint(f"fk_comments_parent_id", "comments", type_="foreignkey")
        op.drop_column("comments", "parent_id")
