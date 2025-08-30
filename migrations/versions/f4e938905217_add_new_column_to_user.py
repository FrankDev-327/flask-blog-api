"""add_new_column_to_user

Revision ID: f4e938905217
Revises: cad8d0672b30
Create Date: 2025-08-30 19:40:53.925674

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = 'f4e938905217'
down_revision = 'cad8d0672b30'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    
    table_name = "users"
    column_name = "password"
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
