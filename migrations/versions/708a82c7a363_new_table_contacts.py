"""new_table_contacts

Revision ID: 708a82c7a363
Revises: 1be5086cd7a1
Create Date: 2025-10-09 21:39:54.087042

"""
import enum
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum

# revision identifiers, used by Alembic.
revision = '708a82c7a363'
down_revision = '1be5086cd7a1'
branch_labels = None
depends_on = None

class StatusFriendEnum(enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    blocked = 'blocked'

def upgrade():    
    op.create_table(
        'contacts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', Enum(StatusFriendEnum), default=StatusFriendEnum.pending, nullable=False),   
        sa.Column('contact_id', sa.Integer(), nullable=False, default=sa.func.now()),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['contact_id'], ['users.id']),
        if_not_exists=True
    )     
      
def downgrade():
    op.drop_table('contacts')
    
