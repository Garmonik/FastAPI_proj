
"""Initial migration

Revision ID: ebfe0243745c
Revises:
Create Date: 2023-04-23 04:37:29.168781

"""
from alembic import op
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Float, JSON, Boolean

# revision identifiers, used by Alembic.
revision = '75ae16699ba5'
down_revision = None
branch_labels = None
depends_on = None




def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        Column("id", Integer(), primary_key=True, index=True),
        Column("email", String(), unique=True, index=True, nullable=False),
        Column("username", String(), unique=True, nullable=True),
        Column("hashed_password", String(length=1024), nullable=False),
        Column("is_active", Boolean(), default=True, nullable=False),
        Column("is_superuser", Boolean(), default=False, nullable=False),
        Column("is_verified", Boolean(), default=False, nullable=False)
    )

    op.create_table(
        "recipes",
        Column("id", Integer(), primary_key=True, index=True),
        Column("title", String(), index=True, nullable=False),
        Column("description", String(), nullable=False),
        Column("ingredients", JSON(), nullable=False),
        Column("guide", JSON(), nullable=False),
        Column("total_time", Integer(), nullable=False),
        Column("rating", Float(), nullable=True),
        Column("author_id", Integer(), ForeignKey("users.id"), nullable=False),
        Column("photo", LargeBinary(), nullable=True),
    )

    op.create_table(
        "ratings",
        Column("id", Integer(), primary_key=True, index=True),
        Column("author_id", Integer(), ForeignKey("users.id"), nullable=False),
        Column("recipe_id", Integer(), ForeignKey("recipes.id"), nullable=False),
        Column("grade", Integer(), nullable=False),
    )

    op.create_table(
        "directions",
        Column("id", Integer(), primary_key=True, index=True),
        Column("description", String(), nullable=False),
        Column("time", Integer(), nullable=False),
        Column("photo", LargeBinary(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ratings")
    op.drop_table("recipes")
    op.drop_table("directions")
    op.drop_table("users")
    # ### end Alembic commands ###
