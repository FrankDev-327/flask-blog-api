"""adding user nick name

Revision ID: b16b6f51fdd7
Revises: f4e938905217
Create Date: 2025-09-03 21:52:14.088390

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = 'b16b6f51fdd7'
down_revision = 'f4e938905217'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    
    table_name = "users"
    column_name = "nick_name"
    columns = [col["name"] for col in inspector.get_columns(table_name)]

    if column_name not in columns:
        op.add_column(table_name, sa.Column(column_name, sa.String(50)))

def downgrade():
    conn = op.get_bind()
    inspector = reflection.Inspector.from_engine(conn)
    
    table_name = "users"
    column_name = "nick_name"
    columns = [col["name"] for col in inspector.get_columns(table_name)]
    
    if column_name in columns:
        op.drop_column(table_name, column_name)
