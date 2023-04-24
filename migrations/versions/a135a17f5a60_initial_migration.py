"""Initial migration

Revision ID: a135a17f5a60
Revises: 
Create Date: 2023-04-23 21:19:11.958080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a135a17f5a60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )

    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('ingredients', sa.ARRAY(sa.String()), nullable=False),
        sa.Column('guide', sa.ARRAY(sa.Integer()), nullable=False),
        sa.Column('total_time', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('photo', sa.LargeBinary(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'directions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('time', sa.Integer(), nullable=False),
        sa.Column('photo', sa.LargeBinary(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'ratings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('grade', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('recipes')
    op.drop_table('ratings')
    op.drop_table('directions')
    op.drop_table('users')
