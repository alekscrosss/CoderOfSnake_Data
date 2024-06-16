"""add user_id column to example_table

Revision ID: fa3401d90b43
Revises: 73dd81e7cbc4
Create Date: 2024-06-16 10:20:44.396459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fa3401d90b43'
down_revision: Union[str, None] = '73dd81e7cbc4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
