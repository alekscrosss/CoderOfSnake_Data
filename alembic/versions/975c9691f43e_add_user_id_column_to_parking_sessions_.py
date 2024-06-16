"""Add user_id column to parking_sessions table

Revision ID: 975c9691f43e
Revises: b3e97449de71
Create Date: 2024-06-14 23:47:10.851682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '975c9691f43e'
down_revision: Union[str, None] = 'b3e97449de71'
branch_labels = None
depends_on = None


def upgrade():
    # Добавление столбца user_id с разрешением NULL значений
    op.add_column('parking_sessions', sa.Column('user_id', sa.Integer(), nullable=True))
    # Создание внешнего ключа для столбца user_id
    op.create_foreign_key('fk_parking_sessions_user_id', 'parking_sessions', 'users', ['user_id'], ['id'])


def downgrade():
    # Удаление внешнего ключа и столбца user_id
    op.drop_constraint('fk_parking_sessions_user_id', 'parking_sessions', type_='foreignkey')
    op.drop_column('parking_sessions', 'user_id')