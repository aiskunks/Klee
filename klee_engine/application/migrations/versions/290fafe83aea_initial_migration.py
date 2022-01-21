"""Initial Migration

Revision ID: 290fafe83aea
Revises: 
Create Date: 2021-09-29 11:31:26.765014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '290fafe83aea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('experiment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('experiment_node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('experiment_id', sa.Integer(), nullable=False),
    sa.Column('module_name', sa.String(length=255), nullable=False),
    sa.Column('input_from', sa.String(length=255), nullable=False),
    sa.Column('report_file_path', sa.String(length=255), nullable=True),
    sa.Column('output_file_path', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('experiment_id', 'module_name', name='unique_module_for_experiment')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('experiment_node')
    op.drop_table('users')
    op.drop_table('experiment')
    # ### end Alembic commands ###
