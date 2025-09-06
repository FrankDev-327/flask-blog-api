"""added_token_table

Revision ID: 79966bb73f0f
Revises: d1319c8cb0b8
Create Date: 2025-09-06 21:33:26.242620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79966bb73f0f'
down_revision = 'd1319c8cb0b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tokens',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('token', sa.Text(), nullable=False, unique=True),
        sa.Column('marked_as_used', sa.Boolean(), default=False),
        if_not_exists=True
    )

def downgrade():
    op.drop_table('tokens')
