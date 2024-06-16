"""Add blacklist

Revision ID: 78ebd6c0bc8b
Revises: 274ece46de2c
Create Date: 2024-06-15 19:14:23.052444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78ebd6c0bc8b'
down_revision: Union[str, None] = '274ece46de2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
