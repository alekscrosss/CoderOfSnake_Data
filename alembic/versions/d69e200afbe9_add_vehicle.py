"""Add vehicle

Revision ID: d69e200afbe9
Revises: d2673f91657c
Create Date: 2024-06-16 09:02:55.105675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd69e200afbe9'
down_revision: Union[str, None] = 'd2673f91657c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
