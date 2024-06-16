"""Add blacklist

Revision ID: 1507b37ef487
Revises: 78ebd6c0bc8b
Create Date: 2024-06-15 19:15:16.356009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1507b37ef487'
down_revision: Union[str, None] = '78ebd6c0bc8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
