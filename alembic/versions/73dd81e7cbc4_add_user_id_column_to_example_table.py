"""add user_id column to example_table

Revision ID: 73dd81e7cbc4
Revises: d69e200afbe9
Create Date: 2024-06-16 10:19:46.681271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73dd81e7cbc4'
down_revision: Union[str, None] = 'd69e200afbe9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
