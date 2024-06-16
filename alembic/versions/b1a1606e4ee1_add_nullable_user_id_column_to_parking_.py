"""Add nullable user_id column to parking_sessions table

Revision ID: b1a1606e4ee1
Revises: 975c9691f43e
Create Date: 2024-06-15 00:04:35.200593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1a1606e4ee1'
down_revision: Union[str, None] = '975c9691f43e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
