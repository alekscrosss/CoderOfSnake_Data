"""Add blacklist

Revision ID: 2d7c137570d0
Revises: 1507b37ef487
Create Date: 2024-06-15 19:15:29.582409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d7c137570d0'
down_revision: Union[str, None] = '1507b37ef487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
