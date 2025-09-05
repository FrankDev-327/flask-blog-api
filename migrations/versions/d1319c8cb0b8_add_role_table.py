"""add_role_table

Revision ID: d1319c8cb0b8
Revises: b16b6f51fdd7
Create Date: 2025-09-05 22:25:35.813978

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1319c8cb0b8'
down_revision = 'b16b6f51fdd7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('role_name', sa.String(length=50), nullable=False), 
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),  
        sa.PrimaryKeyConstraint('id'),    
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        if_not_exists=True    
    )


def downgrade():
    op.drop_table('roles')
