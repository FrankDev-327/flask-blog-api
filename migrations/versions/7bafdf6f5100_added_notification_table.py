"""added_notification_table

Revision ID: 7bafdf6f5100
Revises: 0125e5098897
Create Date: 2025-09-24 18:04:34.208872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bafdf6f5100'
down_revision = '0125e5098897'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('notifications', 
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False), 
        sa.Column('type_notification', sa.String(), nullable=False), 
        sa.Column('notification_preview', sa.String(), nullable=False), 
        sa.Column('user_mentioned_id', sa.Integer(), nullable=False), 
        sa.ForeignKeyConstraint(['user_mentioned_id'], ['users.id']),        
    )

def downgrade():
    op.drop_table('notifications')
