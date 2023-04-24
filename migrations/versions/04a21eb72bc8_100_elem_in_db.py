"""100_elem_in_db

Revision ID: 04a21eb72bc8
Revises: a135a17f5a60
Create Date: 2023-04-24 19:12:22.241391

"""
from random import randint

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '04a21eb72bc8'
down_revision = 'a135a17f5a60'
branch_labels = None
depends_on = None

# Определяем таблицы
recipe_table = table('recipes',
    column('id', sa.Integer()),
    column('title', sa.String()),
    column('description', sa.String()),
    column('ingredients', sa.ARRAY(sa.String())),
    column('guide', sa.ARRAY(sa.Integer())),
    column('total_time', sa.Integer()),
    column('rating', sa.Float()),
    column('author_id', sa.Integer()),
    column('photo', sa.LargeBinary()),
)

direction_table = table('directions',
    column('id', sa.Integer()),
    column('description', sa.String()),
    column('time', sa.Integer()),
    column('photo', sa.LargeBinary()),
)

# Определяем функцию для создания записей
def create_records():
    # Создаем 20 записей в таблице "directions"
    directions = []
    for i in range(20):
        direction = {
            'description': f'Description {i}',
            'time': randint(1, 60),
            'photo': None
        }
        directions.append(direction)
    op.bulk_insert(direction_table, directions)

    # Создаем 100 записей в таблице "recipes"
    recipes = []
    for i in range(100):
        recipe = {
            'title': f'Title {i}',
            'description': f'Description {i}',
            'ingredients': [f'Ingredient {i}-1', f'Ingredient {i}-2', f'Ingredient {i}-3'],
            'guide': [randint(1, 20) for j in range(randint(1, 10))],
            'total_time': randint(1, 120),
            'author_id': 1,
            'photo': None
        }
        recipes.append(recipe)
    op.bulk_insert(recipe_table, recipes)


# Определяем функции миграции
def upgrade():
    create_records()

def downgrade():
    op.execute(recipe_table.delete())
    op.execute(direction_table.delete())