"""new_table_private_message

Revision ID: 1be5086cd7a1
Revises: 22e5f15b6437
Create Date: 2025-10-09 21:30:30.184667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be5086cd7a1'
down_revision = '22e5f15b6437'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'private_message',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('updated_message_at', sa.DateTime(), nullable=True),
        sa.Column('created_message_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id']),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id']),
        if_not_exists=True
    )

def downgrade():
    op.drop_table('private_message')
