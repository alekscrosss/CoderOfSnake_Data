"""Add vehicle

Revision ID: d2673f91657c
Revises: 2d7c137570d0
Create Date: 2024-06-16 08:59:59.033996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2673f91657c'
down_revision: Union[str, None] = '2d7c137570d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
