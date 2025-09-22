"""adding_mention_table

Revision ID: 0125e5098897
Revises: 79966bb73f0f
Create Date: 2025-09-22 21:30:59.841580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0125e5098897'
down_revision = '79966bb73f0f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mentions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('comment_id', sa.Integer(), nullable=False),
        sa.Column('mentioned_user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['mentioned_user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['comment_id'], ['comments.id']),
        if_not_exists=True   
    )

def downgrade():
    op.drop_table('mentions')
