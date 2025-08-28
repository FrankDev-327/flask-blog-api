"""custom column addition

Revision ID: cad8d0672b30
Revises: fab9e0f56653
Create Date: 2025-08-28 18:58:04.895654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cad8d0672b30'
down_revision = 'fab9e0f56653'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('comments', sa.Column('limit_comment', sa.Boolean(), nullable=True, default=False))

def downgrade():
    op.drop_column('comments', 'limit_comment')
